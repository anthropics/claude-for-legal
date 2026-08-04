# billing-stop.ps1
# Stop hook — runs when Claude is about to end the session.
# Blocks only when ALL of: stop_hook_active is false, billing is enabled,
# a per-session timer file exists for this session, and a legal matter is active.
#
# Block format: {"decision":"block","reason":"..."} to stdout, exit 0.
# Non-zero exit surfaces a hook error rather than a clean block.

# --- Parse hook input from stdin ---
$hookInput = $null
try {
    if ([Console]::IsInputRedirected) {
        $raw = [Console]::In.ReadToEnd()
        if ($raw.Trim()) { $hookInput = $raw | ConvertFrom-Json }
    }
} catch { }

# stop_hook_active: true means Claude is already running a hook-induced continuation.
# Blocking again here would trap Claude in an unresolvable loop.
if ($hookInput -and $hookInput.stop_hook_active -eq $true) { exit 0 }

$sessionId = if ($hookInput -and $hookInput.session_id) { $hookInput.session_id } else { $null }

# --- Check billing config ---
$configPath = Join-Path $env:USERPROFILE ".claude\plugins\config\claude-for-legal\billing\CLAUDE.md"
if (-not (Test-Path $configPath)) { exit 0 }

$config = Get-Content $configPath -Raw -ErrorAction SilentlyContinue
if (-not $config -or $config -match '\[PLACEHOLDER\]') { exit 0 }
if ($config -notmatch '\*{0,2}Billing panel at end of session:\*{0,2}\s*enabled') { exit 0 }

# --- Resolve data path ---
$dataPath = $null
if ($config -match '\*{0,2}Data path:\*{0,2}\s*(.+)') {
    $raw = ($matches[1].Trim()) -replace '^\*+', '' -replace '\*+$', ''
    $dataPath = ($raw -replace '^~', $env:USERPROFILE).Trim()
}
if (-not $dataPath) {
    $dataPath = Join-Path $env:USERPROFILE ".claude\plugins\config\claude-for-legal\billing"
}

# --- Resolve attorney slug (set per-machine during cold-start) ---
$attorneySlug = "unknown"
if ($config -match '\*{0,2}Active attorney:\*{0,2}\s*(.+)') {
    $a = ($matches[1].Trim()) -replace '^\*+', '' -replace '\*+$', ''
    if ($a -and $a -notmatch '\[PLACEHOLDER') { $attorneySlug = $a.Split()[0] }
}

# --- Check for this session's timer file ---
# Files are keyed [attorney-slug]_[session-id] so multiple attorneys sharing the
# same billing data path do not interfere with each other's timers.
$sessionsDir = Join-Path $dataPath ".sessions"
$sessionFile = $null

if ($sessionId) {
    $candidate = Join-Path $sessionsDir "${attorneySlug}_${sessionId}"
    if (Test-Path $candidate) { $sessionFile = $candidate }
} else {
    # Fallback when session_id is unavailable: most recent file for this attorney
    if (Test-Path $sessionsDir) {
        $recent = Get-ChildItem $sessionsDir -Filter "${attorneySlug}_*" -ErrorAction SilentlyContinue |
                  Where-Object { $_.LastWriteTime -gt (Get-Date).AddHours(-24) } |
                  Sort-Object LastWriteTime -Descending |
                  Select-Object -First 1
        if ($recent) { $sessionFile = $recent.FullName }
    }
}

if (-not $sessionFile) { exit 0 }  # No active timer for this session

# --- Scan installed legal plugins for an active matter ---
$plugins = @('commercial-legal','ip-legal','corporate-legal','ai-governance-legal','product-legal','litigation-legal')
$activeMatter = $null
$activePlugin = $null
foreach ($plugin in $plugins) {
    $pPath = Join-Path $env:USERPROFILE ".claude\plugins\config\claude-for-legal\$plugin\CLAUDE.md"
    if (Test-Path $pPath) {
        $pContent = Get-Content $pPath -Raw -ErrorAction SilentlyContinue
        if ($pContent -match '\*{0,2}Active matter:\*{0,2}\s*(.+)') {
            $slug = ($matches[1].Trim()) -replace '^\*+', '' -replace '\*+$', ''
            $slug = $slug.Split()[0]
            if ($slug -and $slug -notmatch '^none$') {
                $activeMatter = $slug
                $activePlugin = $plugin
                break
            }
        }
    }
}

if (-not $activeMatter) { exit 0 }

# Include the session file path in the reason so billing-status can delete the right file.
$output = [PSCustomObject]@{
    decision = "block"
    reason   = "Billing panel: matter '$activeMatter' ($activePlugin) is active. Session timer: $sessionFile. Run /billing-legal:billing-status --session-end to log this session's time before closing."
} | ConvertTo-Json -Compress

Write-Output $output
exit 0

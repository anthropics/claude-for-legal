# session-start.ps1
# UserPromptSubmit hook — creates a per-session timer file on the first user message.
# Timer files are keyed [attorney-slug]_[session-id] so multiple attorneys sharing
# the same billing data path do not suppress or overwrite each other's timers.

# --- Parse hook input from stdin ---
$hookInput = $null
try {
    if ([Console]::IsInputRedirected) {
        $raw = [Console]::In.ReadToEnd()
        if ($raw.Trim()) { $hookInput = $raw | ConvertFrom-Json }
    }
} catch { }

# session_id is required to create a unique timer file.
$sessionId = if ($hookInput -and $hookInput.session_id) { $hookInput.session_id } else { $null }
if (-not $sessionId) { exit 0 }

# --- Check billing config ---
$configPath = Join-Path $env:USERPROFILE ".claude\plugins\config\claude-for-legal\billing\CLAUDE.md"
if (-not (Test-Path $configPath)) { exit 0 }

$config = Get-Content $configPath -Raw -ErrorAction SilentlyContinue
if (-not $config -or $config -match '\[PLACEHOLDER\]') { exit 0 }

# --- Resolve data path ---
$dataPath = $null
if ($config -match '\*{0,2}Data path:\*{0,2}\s*(.+)') {
    $raw = ($matches[1].Trim()) -replace '^\*+', '' -replace '\*+$', ''
    $dataPath = ($raw -replace '^~', $env:USERPROFILE).Trim()
}
if (-not $dataPath) {
    $dataPath = Join-Path $env:USERPROFILE ".claude\plugins\config\claude-for-legal\billing"
}

# --- Resolve attorney slug ---
$attorneySlug = "unknown"
if ($config -match '\*{0,2}Active attorney:\*{0,2}\s*(.+)') {
    $a = ($matches[1].Trim()) -replace '^\*+', '' -replace '\*+$', ''
    if ($a -and $a -notmatch '\[PLACEHOLDER') { $attorneySlug = $a.Split()[0] }
}

# --- Create timer file (idempotent — subsequent messages in the same session are no-ops) ---
$sessionsDir = Join-Path $dataPath ".sessions"
$sessionFile = Join-Path $sessionsDir "${attorneySlug}_${sessionId}"

if (-not (Test-Path $sessionFile)) {
    $null = New-Item -ItemType Directory -Path $sessionsDir -Force
    [DateTimeOffset]::UtcNow.ToUnixTimeSeconds() | Set-Content -Path $sessionFile -NoNewline
}

exit 0

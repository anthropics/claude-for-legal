# activity-log.ps1
# PostToolUse hook — silently appends file operations to a per-session activity log.
# Fires after every tool call. Only records Edit/Write/Read on non-billing files
# when a session timer is active (i.e., a matter is open and billing is running).
#
# Output: none (this hook never blocks or injects text)
# Log format: ISO8601_TIMESTAMP|TOOL_NAME|FILENAME
# Log location: [billing_data_path]/.sessions/[attorney-slug]_[session-id]_activity

# --- Parse hook input from stdin ---
$hookInput = $null
try {
    if ([Console]::IsInputRedirected) {
        $raw = [Console]::In.ReadToEnd()
        if ($raw.Trim()) { $hookInput = $raw | ConvertFrom-Json }
    }
} catch { }

# Only record Edit, Write, and Read tool calls
$trackedTools = @('Edit', 'Write', 'Read')
$toolName = if ($hookInput -and $hookInput.tool_name) { $hookInput.tool_name } else { $null }
if (-not $toolName -or $toolName -notin $trackedTools) { exit 0 }

$sessionId = if ($hookInput -and $hookInput.session_id) { $hookInput.session_id } else { $null }
if (-not $sessionId) { exit 0 }

# --- Check billing config ---
$configPath = Join-Path $env:USERPROFILE ".claude\plugins\config\claude-for-legal\billing\CLAUDE.md"
if (-not (Test-Path $configPath)) { exit 0 }

$config = Get-Content $configPath -Raw -ErrorAction SilentlyContinue
if (-not $config -or $config -match '\[PLACEHOLDER\]') { exit 0 }
if ($config -notmatch '\*{0,2}Activity logging:\*{0,2}\s*enabled') { exit 0 }

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

# --- Check that a session timer file exists (billing is active for this session) ---
$sessionsDir = Join-Path $dataPath ".sessions"
$timerFile = Join-Path $sessionsDir "${attorneySlug}_${sessionId}"
if (-not (Test-Path $timerFile)) { exit 0 }

# --- Extract the file path from tool input ---
$filePath = $null
if ($hookInput.tool_input -and $hookInput.tool_input.file_path) {
    $filePath = $hookInput.tool_input.file_path
}
if (-not $filePath) { exit 0 }

# --- Skip billing data files (don't log reads/writes to our own YAML registers) ---
$normalizedPath = $filePath.ToLower() -replace '/', '\'
$normalizedData = $dataPath.ToLower() -replace '/', '\'
$billingConfigDir = (Join-Path $env:USERPROFILE ".claude\plugins\config\claude-for-legal").ToLower()

if ($normalizedPath.StartsWith($normalizedData)) { exit 0 }
if ($normalizedPath.StartsWith($billingConfigDir)) { exit 0 }

# --- Extract just the filename for the log (avoid leaking full paths to shared billing data) ---
$fileName = Split-Path $filePath -Leaf

# --- Append to activity log ---
$activityLog = Join-Path $sessionsDir "${attorneySlug}_${sessionId}_activity"
$timestamp = [DateTimeOffset]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")
$logLine = "${timestamp}|${toolName}|${fileName}"

try {
    $null = New-Item -ItemType Directory -Path $sessionsDir -Force
    Add-Content -Path $activityLog -Value $logLine -NoNewline:$false -Encoding utf8
} catch { }

exit 0

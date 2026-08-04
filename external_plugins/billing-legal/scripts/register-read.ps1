# register-read.ps1
# Deterministic reader and validator for the billing time register.
#
# Skills call this instead of reading and totalling time-register.yaml themselves.
# It resolves the data path from config, confirms the register exists, parses every
# entry, checks the invariants the register is supposed to hold, and emits JSON.
#
# The point is that the numbers a skill reports come from a program rather than from
# a model's arithmetic or its memory of an earlier turn. If this script did not run,
# there is no output to report from.
#
# Usage:
#   register-read.ps1 [-DataPath <path>] [-Client <slug>] [-Attorney <slug>] [-Status <status>]
#
# Exit codes:
#   0  register read and valid
#   2  register file is absent (different from empty -- see below)
#   3  register parsed but failed one or more invariants
#   4  config missing, unreadable, or still contains placeholders
#
# On 0 and 3 a JSON object goes to stdout. On 2 and 4 the reason goes to stderr and
# stdout stays empty, so a caller cannot mistake an error for a result.
#
# Absent is not the same condition as empty. An empty or comment-only register is the
# normal state of a fresh install and exits 0 with zero entries. A missing file means
# the data path is wrong, a shared folder has not synced, or something removed it.

[CmdletBinding()]
param(
    [string]$DataPath,
    [string]$Client,
    [string]$Attorney,
    [string]$Status
)

$ErrorActionPreference = 'Stop'

function Fail([int]$Code, [string]$Message) {
    [Console]::Error.WriteLine($Message)
    exit $Code
}

# --- Resolve the data path -------------------------------------------------
# Prefixed script-scope names: this file may be dot-sourced, and dot-sourcing runs
# in the caller's scope where a bare $Config or $Root would clobber theirs.

if (-not $DataPath) {
    $script:RegReadConfigPath = Join-Path $env:USERPROFILE ".claude\plugins\config\claude-for-legal\billing\CLAUDE.md"
    if (-not (Test-Path $script:RegReadConfigPath)) {
        Fail 4 "No billing config at $($script:RegReadConfigPath). Run /billing-legal:cold-start-interview."
    }

    $script:RegReadConfig = Get-Content $script:RegReadConfigPath -Raw -Encoding UTF8
    if (-not $script:RegReadConfig) { Fail 4 "Billing config is empty: $($script:RegReadConfigPath)" }
    if ($script:RegReadConfig -match '\[PLACEHOLDER\]') {
        Fail 4 "Billing config still contains [PLACEHOLDER] values. Run /billing-legal:cold-start-interview."
    }

    if ($script:RegReadConfig -match '\*{0,2}Data path:\*{0,2}\s*(.+)') {
        $script:RegReadRaw = ($matches[1].Trim()) -replace '^\*+', '' -replace '\*+$', ''
        $DataPath = ($script:RegReadRaw -replace '^~', $env:USERPROFILE).Trim()
    }
    if (-not $DataPath) {
        $DataPath = Join-Path $env:USERPROFILE ".claude\plugins\config\claude-for-legal\billing"
    }
}

$script:RegReadFile = Join-Path $DataPath "time-register.yaml"

if (-not (Test-Path $script:RegReadFile)) {
    Fail 2 ("No time register at $($script:RegReadFile). The file is absent, not empty. " +
            "Billing data may be unsynced, the data path may be wrong, or the file may have been moved. " +
            "Do not report figures from memory.")
}

# --- Read, stripping any BOM ----------------------------------------------
# PowerShell 5.1 Out-File -Encoding utf8 writes a BOM, so the register may carry one.
# Strip it before any regex anchored at the start of the text.

$script:RegReadText = [System.IO.File]::ReadAllText($script:RegReadFile, [System.Text.Encoding]::UTF8)
$script:RegReadText = $script:RegReadText.TrimStart([char]0xFEFF)
$script:RegReadLines = $script:RegReadText -split "`r?`n"

# --- Parse -----------------------------------------------------------------
# Format is fixed by the skills: each entry is a top-level list item beginning
# "- id: " at column 0, followed by two-space-indented "key: value" lines. Parsing
# it directly avoids a YAML dependency; the plugin ships no runtime dependencies.

$script:RegReadEntries = New-Object System.Collections.ArrayList
$script:RegReadErrors  = New-Object System.Collections.ArrayList
$script:RegReadCurrent = $null
$script:RegReadLineNo  = 0

foreach ($line in $script:RegReadLines) {
    $script:RegReadLineNo++
    if ($line -match '^\s*#') { continue }
    if ($line.Trim() -eq '') { continue }

    if ($line -match '^- id:\s*(.+)$') {
        if ($script:RegReadCurrent) { [void]$script:RegReadEntries.Add($script:RegReadCurrent) }
        $script:RegReadCurrent = [ordered]@{ id = $matches[1].Trim(); _line = $script:RegReadLineNo }
        continue
    }

    if ($line -match '^\s+([a-z_]+):\s*(.*)$') {
        if (-not $script:RegReadCurrent) {
            [void]$script:RegReadErrors.Add("line $($script:RegReadLineNo): field outside any entry")
            continue
        }
        $k = $matches[1]
        $v = $matches[2].Trim()
        if ($v -eq 'null' -or $v -eq '') { $v = $null }
        elseif ($v.StartsWith('"') -and $v.EndsWith('"') -and $v.Length -ge 2) { $v = $v.Substring(1, $v.Length - 2) }
        $script:RegReadCurrent[$k] = $v
        continue
    }

    if ($line -match '^\S' -and $line -notmatch '^- id:') {
        [void]$script:RegReadErrors.Add("line $($script:RegReadLineNo): unexpected top-level content '$($line.Trim())'")
    }
}
if ($script:RegReadCurrent) { [void]$script:RegReadEntries.Add($script:RegReadCurrent) }

# --- Validate invariants ---------------------------------------------------

$script:RegReadKnownStatus = @('pending','approved','billed','write-off')
$script:RegReadSeenIds = @{}

foreach ($e in $script:RegReadEntries) {
    $id = $e.id
    $ln = $e._line

    if ($script:RegReadSeenIds.ContainsKey($id)) {
        [void]$script:RegReadErrors.Add("line ${ln}: duplicate entry id '$id'")
    }
    $script:RegReadSeenIds[$id] = $true

    foreach ($required in @('date','attorney','client','hours','rate','amount','status')) {
        if (-not $e.Contains($required) -or $null -eq $e[$required]) {
            [void]$script:RegReadErrors.Add("line ${ln}: entry '$id' missing required field '$required'")
        }
    }

    if ($e['status'] -and ($script:RegReadKnownStatus -notcontains $e['status'])) {
        [void]$script:RegReadErrors.Add("line ${ln}: entry '$id' has unknown status '$($e['status'])'")
    }

    if ($e['date'] -and ($e['date'] -notmatch '^\d{4}-\d{2}-\d{2}$')) {
        [void]$script:RegReadErrors.Add("line ${ln}: entry '$id' date '$($e['date'])' is not YYYY-MM-DD")
    }

    # amount must equal hours * rate. This is the check a model doing mental arithmetic
    # cannot be relied on to make, and it is the one that catches a hand-edited register.
    if ($null -ne $e['hours'] -and $null -ne $e['rate'] -and $null -ne $e['amount']) {
        $h = 0.0; $r = 0.0; $a = 0.0
        $okH = [double]::TryParse($e['hours'], [ref]$h)
        $okR = [double]::TryParse($e['rate'],  [ref]$r)
        $okA = [double]::TryParse($e['amount'],[ref]$a)
        if (-not ($okH -and $okR -and $okA)) {
            [void]$script:RegReadErrors.Add("line ${ln}: entry '$id' has non-numeric hours, rate, or amount")
        } else {
            $expected = [math]::Round($h * $r, 2)
            if ([math]::Abs($expected - $a) -gt 0.005) {
                [void]$script:RegReadErrors.Add("line ${ln}: entry '$id' amount $a does not equal hours $h x rate $r (expected $expected)")
            }
        }
    }
}

# --- Filter ----------------------------------------------------------------

$script:RegReadFiltered = $script:RegReadEntries
if ($Client)   { $script:RegReadFiltered = @($script:RegReadFiltered | Where-Object { $_['client']   -eq $Client }) }
if ($Attorney) { $script:RegReadFiltered = @($script:RegReadFiltered | Where-Object { $_['attorney'] -eq $Attorney }) }
if ($Status)   { $script:RegReadFiltered = @($script:RegReadFiltered | Where-Object { $_['status']   -eq $Status }) }

# --- Totals ----------------------------------------------------------------

function Sum-Amount($rows) {
    $t = 0.0
    foreach ($row in $rows) {
        $v = 0.0
        if ([double]::TryParse($row['amount'], [ref]$v)) { $t += $v }
    }
    return [math]::Round($t, 2)
}
function Sum-Hours($rows) {
    $t = 0.0
    foreach ($row in $rows) {
        $v = 0.0
        if ([double]::TryParse($row['hours'], [ref]$v)) { $t += $v }
    }
    return [math]::Round($t, 2)
}

$script:RegReadWip = @($script:RegReadFiltered | Where-Object { $_['status'] -eq 'pending' -or $_['status'] -eq 'approved' })

$script:RegReadOut = [ordered]@{
    register_path   = $script:RegReadFile
    data_path       = $DataPath
    entry_count     = $script:RegReadEntries.Count
    filtered_count  = @($script:RegReadFiltered).Count
    filters         = [ordered]@{ client = $Client; attorney = $Attorney; status = $Status }
    totals          = [ordered]@{
        hours          = Sum-Hours   $script:RegReadFiltered
        amount         = Sum-Amount  $script:RegReadFiltered
        wip_hours      = Sum-Hours   $script:RegReadWip
        wip_amount     = Sum-Amount  $script:RegReadWip
    }
    by_status       = [ordered]@{}
    valid           = ($script:RegReadErrors.Count -eq 0)
    errors          = @($script:RegReadErrors)
    entries         = @($script:RegReadFiltered | ForEach-Object {
                          $copy = [ordered]@{}
                          foreach ($k in $_.Keys) { if ($k -ne '_line') { $copy[$k] = $_[$k] } }
                          [pscustomobject]$copy })
}

foreach ($s in $script:RegReadKnownStatus) {
    $rows = @($script:RegReadFiltered | Where-Object { $_['status'] -eq $s })
    $script:RegReadOut.by_status[$s] = [ordered]@{
        count  = $rows.Count
        hours  = Sum-Hours  $rows
        amount = Sum-Amount $rows
    }
}

[Console]::Out.WriteLine((ConvertTo-Json $script:RegReadOut -Depth 6 -Compress))

if ($script:RegReadErrors.Count -gt 0) { exit 3 }
exit 0

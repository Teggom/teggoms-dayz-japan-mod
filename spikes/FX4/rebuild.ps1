# FX4 rebuild (sequential, <= 4 processes at a time): jp_common pack, parts, buildings, furniture + site props.
$ErrorActionPreference = "Continue"
Set-Location D:\DayZ-Server_AI-20260907-MultiMap\japan_dev
$L = "spikes\FX4\_build"
New-Item -ItemType Directory -Force $L | Out-Null
function step($name, $cmd) {
    $t0 = Get-Date
    "=== $name START $($t0.ToString('HH:mm:ss'))" | Out-File -Append -Encoding utf8 "$L\rebuild.log"
    cmd /c "$cmd > $L\$name.log 2>&1"
    "=== $name END exit $LASTEXITCODE ($([int]((Get-Date) - $t0).TotalSeconds) s)" | Out-File -Append -Encoding utf8 "$L\rebuild.log"
}
# jp_common: pack it BY HAND first (this quoting failed under cmd /c on 2026-10-01):
#   cd research\materials; python -c "import build_materials as BM; print(BM.pack())"
step "parts" "python parts\kit\build_parts.py"
step "pipeline" "python buildings\pipeline.py --jobs 4"
step "b3a" "python spikes\B3a\build.py"
step "l1" "python spikes\L1\build_l1.py"
step "s1" "python spikes\S1\build_s1.py"
step "w2f" "python spikes\W2F\build_w2f.py"
step "b3b" "python spikes\B3b\build.py"
step "l2" "python spikes\L2\build_l2.py"
step "asm" "python tools\assemble_config.py --pack"
"=== ALL DONE" | Out-File -Append -Encoding utf8 "$L\rebuild.log"

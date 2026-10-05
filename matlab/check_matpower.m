%CHECK_MATPOWER  MATLAB · MATPOWER 환경 점검
%   MATLAB 에서:  cd C:\LMP\matlab  →  check_matpower

here = fileparts(mfilename('fullpath'));
addpath(fullfile(here, '..', 'data', 'raw'));       % pglib_opf_case118_ieee.m
ok = true;

if exist('rundcopf', 'file') ~= 2
    fprintf('[실패] MATPOWER 를 찾을 수 없습니다 → MATPOWER 폴더에서 install_matpower 실행\n');
    return
end
fprintf('[성공] MATPOWER %s (MATLAB %s)\n', mpver, version('-release'));

define_constants;
mpopt = mpoption('verbose', 0, 'out.all', 0);

r = rundcopf(case3_lecture, mpopt);
lmp = round(r.bus(:, LAM_P)', 2);
pass = r.success && isequal(lmp, [20 50 80]);
ok = ok && pass;
fprintf('[%s] 3-bus 강의 예제 LMP = [%s]  (기대값 [20 50 80])\n', ternary(pass), num2str(lmp));

mpc = loadcase('pglib_opf_case118_ieee');
r = rundcopf(mpc, mpopt);
pass = r.success && size(mpc.bus, 1) == 118 && size(mpc.branch, 1) == 186;
ok = ok && pass;
fprintf('[%s] IEEE 118 계통 (버스 %d, 발전기 %d, 선로 %d) DC-OPF 수렴\n', ternary(pass), ...
    size(mpc.bus, 1), size(mpc.gen, 1), size(mpc.branch, 1));

% 제출 도구(tools/submit.py)는 Python 이 필요하다
[st, ~] = system('python -c "import pandas, cryptography"');
pass = st == 0;
ok = ok && pass;
fprintf('[%s] 제출용 Python (pandas, cryptography)\n', ternary(pass));

if ok
    fprintf('\n모든 점검 통과! 과제를 시작하세요.\n');
else
    fprintf('\n[실패] 줄을 AI 에게 그대로 붙여넣어 물어보세요.\n');
end

function s = ternary(p)
    if p, s = '성공'; else, s = '실패'; end
end

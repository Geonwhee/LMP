%LECTURE_3BUS  강의 3-bus 예제를 MATPOWER 로 계산한다.
%   MATLAB 에서:  cd C:\LMP\matlab  →  lecture_3bus
%   기대 결과: G1 = 180 MW, G2 = 120 MW, LMP = [20 50 80] $/MWh, 선로 1-3 만 혼잡

define_constants;                                  % LAM_P, PF, MU_SF ... (열 번호는 1부터)
mpopt = mpoption('verbose', 0, 'out.all', 0);      % 화면 출력 끄기
r = rundcopf(case3_lecture, mpopt);                % DC 최적조류 (DC-OPF)
fprintf('수렴: %d\n', r.success);

fprintf('\n[발전기]\n');
for k = 1:size(r.gen, 1)
    fprintf('  버스 %d: %7.1f MW\n', r.gen(k, GEN_BUS), r.gen(k, PG));
end

fprintf('\n[노드별 가격 LMP]\n');
for k = 1:size(r.bus, 1)
    fprintf('  버스 %d: %6.2f $/MWh\n', r.bus(k, BUS_I), r.bus(k, LAM_P));
end

fprintf('\n[선로]\n');
for k = 1:size(r.branch, 1)
    mu = r.branch(k, MU_SF) + r.branch(k, MU_ST);  % 0 보다 크면 혼잡 선로
    fprintf('  %d-%d: 조류 %7.1f MW / 한계 %5.0f MW   쉐도우 프라이스 mu = %5.1f\n', ...
        r.branch(k, F_BUS), r.branch(k, T_BUS), r.branch(k, PF), r.branch(k, RATE_A), mu);
end

% 답안 CSV 저장 예시 (형식은 Python 과 같음: 열 이름 bus, lmp)
% T = table(r.bus(:, BUS_I), r.bus(:, LAM_P), 'VariableNames', {'bus', 'lmp'});
% writetable(T, fullfile('..', 'answers', 'task1_lmp.csv'));

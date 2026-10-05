function mpc = case3_lecture
%CASE3_LECTURE  강의 3-bus 예제 (모든 선로 리액턴스 동일)
%   버스1: G1 20 $/MWh (slack) · 버스2: G2 50 $/MWh · 버스3: 부하 300 MW
%   선로 1-3 만 열용량 160 MW
%   강의 결과: G1 = 180, G2 = 120, LMP = [20 50 80] $/MWh

mpc.version = '2';
mpc.baseMVA = 100;

%  bus_i type Pd Qd Gs Bs area Vm Va baseKV zone Vmax Vmin
mpc.bus = [
    1 3   0 0 0 0 1 1 0 230 1 1.1 0.9;
    2 2   0 0 0 0 1 1 0 230 1 1.1 0.9;
    3 1 300 0 0 0 1 1 0 230 1 1.1 0.9;
];

%  bus Pg Qg Qmax Qmin Vg mBase status Pmax Pmin
mpc.gen = [
    1 0 0 300 -300 1 100 1 300 0;
    2 0 0 300 -300 1 100 1 300 0;
];

%  fbus tbus r x b rateA rateB rateC ratio angle status angmin angmax
mpc.branch = [
    1 2 0 0.1 0 500 500 500 0 0 1 -360 360;
    1 3 0 0.1 0 160 160 160 0 0 1 -360 360;
    2 3 0 0.1 0 500 500 500 0 0 1 -360 360;
];

%  model startup shutdown n c1 c0   (선형 비용 20 P, 50 P)
mpc.gencost = [
    2 0 0 2 20 0;
    2 0 0 2 50 0;
];

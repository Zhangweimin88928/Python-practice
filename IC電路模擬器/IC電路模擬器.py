import pathlib
import time


def AND(*args):
    for i in args:
        if i == 0:
            return 0
    return 1


def OR(*args):
    for i in args:
        if i == 1:
            return 1
    return 0


def XOR(*args):
    return 1 if sum(args) % 2 == 1 else 0


def NOR(*args):
    return 1-OR(*args)


def NOT(arg):
    return 1-arg


def NAND(*args):
    return 1-AND(*args)


def XNOR(*args):
    return 1-XOR(*args)


def BUF(arg):
    return arg


class BasicSim:

    def __init__(self, benchFile):
        self.gate_value = {}
        self.input_list = []
        self.output_list = []
        self.gate_list = []
        self.benchFile = benchFile

    def parse_bench(self):
        with open(self.benchFile, 'r') as f:
            while line := f.readline():
                if line.startswith('#') or len(line.strip()) == 0:
                    continue
                if line.startswith('INPUT'):
                    gName = line.split('(')[1].replace(')', '').strip()
                    self.input_list.append(gName)
                    self.gate_value[gName] = None
                elif line.startswith('OUTPUT'):
                    gName = line.split('(')[1].replace(')', '').strip()
                    self.output_list.append(gName)
                    self.gate_value[gName] = None
                else:
                    line = line\
                        .replace(' ', '')\
                        .replace('=', ',')\
                        .replace('(', ',')\
                        .replace(')', '')\
                        .strip()
                    tt = line.split(',')
                    self.gate_list.append(tt)
                    self.gate_value[tt[0]] = None

    def doSim(self, gateInfo):
        gName = gateInfo[0]
        gateType = gateInfo[1]
        v = 0
        match gateType:
            case 'and':
                v = AND(*[self.gate_value[i] for i in gateInfo[2:]])
            case 'or':
                v = OR(*[self.gate_value[i] for i in gateInfo[2:]])
            case 'xor':
                v = XOR(*[self.gate_value[i] for i in gateInfo[2:]])
            case 'nor':
                v = NOR(*[self.gate_value[i] for i in gateInfo[2:]])
            case 'not':
                v = NOT(self.gate_value[gateInfo[2]])
            case 'nand':
                v = NAND(*[self.gate_value[i] for i in gateInfo[2:]])
            case 'xnor':
                v = XNOR(*[self.gate_value[i] for i in gateInfo[2:]])
            case 'buf':
                v = BUF(self.gate_value[gateInfo[2]])

        self.gate_value[gName] = v

    def fillInput(self, ipLine: str):
        if len(ipLine) != len(self.input_list):
            raise Exception('input line length not match')
        for i in range(len(self.input_list)):
            self.gate_value[self.input_list[i]] = int(ipLine[i])

    def gatherOutput(self, ipLine: str):
        return '{} {}\n'.format(ipLine, ''.join([str(self.gate_value[i]) for i in self.output_list]))

    def simulation(self, ipFile, opFile):
        self.parse_bench()
        result = ''
        with open(ipFile, 'r') as f:
            while line := f.readline().strip():
                self.fillInput(line)
                for gateInfo in self.gate_list:
                    self.doSim(gateInfo)
                result += self.gatherOutput(line)

        with open(opFile, 'w') as f:
            f.write(result)

    def compare(self, opFile, ansFile):
        with open(opFile, 'r') as f1, open(ansFile, 'r') as f2:
            op = f1.readlines()
            answer = f2.readlines()
            if len(op) != len(answer):
                raise Exception('output line length not match')
            for i in range(len(op)):
                if op[i] != answer[i]:
                    print('line {} not match'.format(i+1))
                    print('op: {}'.format(op[i]))
                    print('answer: {}'.format(answer[i]))
                    return False
        return True


if __name__ == '__main__':
    ic = 'c2670'
    count = '10k'
    path = pathlib.Path('C://data')
    sim = BasicSim(path/f'{ic}.bench.txt')
    
    start = time.time()
    
    sim.simulation(path/f'{ic}_{count}_ip.txt', path/f'{ic}_{count}_op.txt')
    print(sim.compare(path/f'{ic}_{count}_op.txt',
          path/f'{ic}_{count}_op.txt'))
    
    print(f'{time.time()-start:.1f}')

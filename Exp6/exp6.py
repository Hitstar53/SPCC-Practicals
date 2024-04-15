from prettytable import PrettyTable
def find_basic_blocks(code):
    basic_blocks = []
    current_block = []

    for line in range(len(code)):
        if code[line].startswith('LABEL'):
            if current_block:
                basic_blocks.append(current_block)
                current_block = []
            current_block.append(code[line])
        elif code[line-1].startswith('IF'):
            basic_blocks.append(current_block)
            current_block = [code[line]]
        else:
            current_block.append(code[line])

    if current_block:
        basic_blocks.append(current_block)

    return basic_blocks


def generate_flow_graph(basic_blocks):
    flow_graph = {}
    block_number = 1
    for block_num, block in enumerate(basic_blocks):
        successors = []
        for line_num in range(len(block)):
            if 'GOTO' in block[line_num]:
                goto_block = block[line_num].split()[-1]
                goto_block_num = None
                for i, blk in enumerate(basic_blocks):
                    if blk[0].split()[1] == goto_block:
                        goto_block_num = i + 1
                        break
                if goto_block_num is not None:
                    successors.append(goto_block_num)
            elif block[-1].startswith('IF'):
                if block_num +2 not in successors:
                    successors.append(block_num + 2)
            elif block[line_num].startswith('IF') or (line_num > 0 and block[line_num-1].startswith('IF')):
                conditions = block[line_num].split()[2:]
                for condition in conditions:
                    goto_block = condition.split(':')[1]
                    goto_block_num = None
                    for i, blk in enumerate(basic_blocks):
                        if blk[0].split()[1] == goto_block:
                            goto_block_num = i + 1
                            break
                    if goto_block_num is not None:
                        successors.append(goto_block_num)

        flow_graph[block_number] = successors
        block_number += 1 
        
    return flow_graph

def main():
    code = [
        'LABEL L1',
        'A = B + C',
        'IF A > 0 GOTO L3',
        'D = E + F',
        'GOTO L2',
        'LABEL L3',
        'G = H + I',
        'IF G > 0 GOTO L4',
        'J = K + L',
        'LABEL L4',
        'M = N + O',
        'LABEL L2',
        'P = Q + R'
    ]

    basic_blocks = find_basic_blocks(code)
    table = PrettyTable()
    print("Basic Blocks:")
    table.field_names = ["Block Number", "Lines"]
    for i in range(len(basic_blocks)):
        table.add_row([i+1, basic_blocks[i]])
    print(table)
    flow_graph = generate_flow_graph(basic_blocks)
    table = PrettyTable()
    table.field_names = ["Block Number", "Successors"]
    for block_num, successors in flow_graph.items():
        table.add_row([block_num, successors])
    print("Flow Graph:")
    print(table)

if __name__ == "__main__":
    main()
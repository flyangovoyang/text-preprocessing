# caution: last sentence should end with two blank lines.
def conver_bio_to_bmes():
    """ convert BIO schema to BMES tagging schema"""
    input_file_path = 'test.txt'
    output_file_path = 'test.data'
    
    with open(output_file_path, 'w', encoding='utf8') as fout:
        sent = []
        bmes = []
        label = []
        with open(input_file_path, 'r', encoding='utf8') as fin:
            for line in fin:
                line = line.strip()
                if not line:
                    # change bio -> bmes
                    for index, token in enumerate(bmes):
                        if token == 'B':
                            # O B O x x -> O S O x x
                            # B -> S
                            # x x B -> x x S
                            # B x x -> S x x
                            if (0 < index < len(label) - 1 and bmes[index - 1] == 'O' and bmes[index + 1] == 'O') \
                                    or (len(label) == 1) or (index == len(label) - 1) or (index == 0 and bmes[index + 1] == 'O'):
                                bmes[index] = 'S'
                        elif token == 'I':
                            # x x I -> B E x x
                            # x x I O/B -> B E O
                            if index == len(label)-1 or (index < len(label)-1 and bmes[index+1] != 'I'):
                                bmes[index] = 'E'
                            # x x I I -> x x M I
                            elif index < len(label)-1 and bmes[index+1] == 'I':
                                bmes[index] = 'M'
                    for s, b, l in zip(sent, bmes, label):
                        if b != 'O':
                            fout.write('{} {}-{}\n'.format(s, b, l))
                        else:
                            fout.write('{} {}\n'.format(s, b))
                    fout.write('\n')
                    sent = []
                    bmes = []
                    label = []
                else:
                    ll = line.split()
                    sent.append(ll[0])
                    if ll[1] == 'O':
                        bmes.append('O')
                        label.append('O')
                    else:
                        bmes.append(ll[1].split('-')[0])
                        label.append(ll[1].split('-')[1])


def convert_horizontal_to_vertical(input_file_path, output_file_path):
    """ notice split('####')[x] should be modified according the acutal circumstance """
    with open(output_file_path, 'w', encoding='utf8') as fout:
        with open(input_file_path, 'r', encoding='utf8') as fin:
            for line in fin:
                line = line.strip()
                if not line:
                    continue
                else:
                    part = line.split('####')[2]
                    pairs = part.split()
                    for pair in pairs:
                        ch = pair.split('=')[0]
                        tag = pair.split('=')[1]
                        fout.write('{} {}\n'.format(ch, tag))
                    fout.write('\n')

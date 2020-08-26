import re
import time


class LineBlock:
    """ each line in markdown file will be parsed to LineBlock object """
    def __init__(self, btype, content=None):
        assert btype in ['text', 'ul', 'quote', 'empty', 'code_s_e', 'code_s', 'title1', 'title2', 'title3', 'title4',
                         'title5', 'title6'], 'unknown LineBlock type:{}'.format(btype)
        self.btype = btype  # []
        if content is None:
            self.content = ''
        else:
            assert isinstance(content, str), 'LineBlock content should be str'
            self.content = content

    def __repr__(self):
        return '({}: "{}")'.format(self.btype, self.content)


class HtmlBlock:
    """ each btype will be converted to a html tag(represented as a HtmlBlock object) """
    def __init__(self, btype, contents=None):
        assert btype in ['text', 'ul', 'quote', 'code', 'title1', 'title2', 'title3', 'title4', 'title5', 'title6'], \
            'unknown HtmlBlock type:{}'.format(btype)
        self.btype = btype
        if contents is None:
            self.contents = []
        else:
            assert isinstance(contents, list), 'HtmlBlock contents should be list'
            self.contents = contents

    def __repr__(self):
        if self.btype == 'empty':
            return '[empty]'
        else:
            return '[{}: {}]'.format(self.btype, self.contents)


def build_blocks_from_md_file(md_file_path):
    """ get line blocks from markdown file """
    stack = []
    with open(md_file_path, 'r', encoding='utf8') as fin:
        for line in fin:
            line = line.rstrip()
            if not line:
                stack.append(LineBlock('empty'))
            elif line.startswith('######'):
                stack.append(LineBlock('title6', line))
            elif line.startswith('#####'):
                stack.append(LineBlock('title5', line))
            elif line.startswith('####'):
                stack.append(LineBlock('title4', line))
            elif line.startswith('###'):
                stack.append(LineBlock('title3', line))
            elif line.startswith('##'):
                stack.append(LineBlock('title2', line))
            elif line.startswith('#'):
                stack.append(LineBlock('title1', line))
            elif re.match(r'>.*', line):
                stack.append(LineBlock('quote', re.findall(r'>(.*)', line)[0]))
            elif line.startswith('- '):
                stack.append(LineBlock('ul', line[2:]))
            elif line == '```':
                stack.append(LineBlock('code_s_e'))
            elif line.startswith('```'):
                stack.append(LineBlock('code_s', line))
            else:
                stack.append(LineBlock('text', line))
    return stack


def smooth_blocks(blocks):
    """ merge and map line blocks into html blocks """
    mode = 'none'  # code, text, ul, quote
    stack = []

    after = []  # smooth result
    # text, empty, title1-6, codeblock_s, codeblock_s_e, ul, quote
    for i, block in enumerate(blocks):
        if mode == 'code':
            # end of the code mode
            if block.btype == 'code_s_e':
                after.append(HtmlBlock(mode, [x.content for x in stack]))
                stack = []
                mode = 'none'
            # not code end
            else:
                block.btype = 'code'
                stack.append(block)
        else:  # not code
            if block.btype.startswith('title'):
                if mode != block.btype and mode != 'none':
                    after.append(HtmlBlock(mode, [x.content for x in stack]))
                    stack = []
                after.append(HtmlBlock(block.btype, [block.content]))
                mode = 'none'
            elif block.btype in ['text', 'ul', 'quote']:
                if mode != block.btype and mode != 'none':
                    after.append(HtmlBlock(mode, [x.content for x in stack]))
                    stack = []
                stack.append(block)
                mode = block.btype
            elif block.btype == 'empty':
                if mode != 'none':
                    after.append(HtmlBlock(mode, [x.content for x in stack]))
                    stack = []
                    mode = 'none'
            elif block.btype == 'code_s' or block.btype == 'code_s_e':
                if mode != 'none':
                    after.append(HtmlBlock(mode, [x.content for x in stack]))
                    stack = []
                stack.append(block)
                mode = 'code'
            else:
                assert 0, 'unknow block btype'
    if stack and mode != 'none':
        after.append(HtmlBlock(mode, [x.content for x in stack]))
    return after


def generate_html(htmlblocks, attrs):
    """ generate html draft according to the html blocks """
    s = '''<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
	<meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="../../css/bootstrap.min.css">
    <link rel="stylesheet" href="../../css/''' + attrs['css_file'] + '''">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css" integrity="sha384-AfEj0r4/OFrOo5t7NnNe46zW/tFgW6x/bCJG8FqQCEo3+Aro6EYUG4+cU+KJWu/X" crossorigin="anonymous">
    <!-- katex formular render engine -->
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js" integrity="sha384-g7c+Jr9ZivxKLnZTDUhnkOnsh30B4H0rpLUpJ4jAIKs4fnJI+sEnkvrMWph2EDg4" crossorigin="anonymous"></script>
    <script>
        function my_render(){
            var my_options = {delimiters:[{left: "$$", right: "$$", display: true}, {left: "$", right: "$", display: false}]};
            renderMathInElement(document.body, my_options);
        }
    </script>
    <!-- To automatically render math in text elements, include the auto-render extension: -->
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/contrib/auto-render.min.js" integrity="sha384-mll67QQFJfxn0IYznZYonOWZ644AWYC+Pt2cHqMaRhXVrursRwvLnLaebdGIlYNa" crossorigin="anonymous" onload="my_render()"></script>
</head>
<body>
    <div class="container">
        <div class="header">
            <p><a href="../../''' + attrs['index_page'] + '''">< 返回首页</a></p>
        </div>
        <div class="text-center">
            <h1>''' + attrs['blog_title'] + '''</h1>
            <p>''' + attrs['create_time'] + '''</p>
            <hr>
        </div>
    '''

    for block in htmlblocks:
        if block.btype == 'text':
            s += '<p>' + ' '.join(block.contents) + '</p>'
        elif block.btype.startswith('title'):
            grade = block.btype[-1]
            s += '<h' + str(grade) + '>' + block.contents[0][int(block.btype[-1]):].lstrip() + '</h' + str(grade) + '>'
        elif block.btype == 'quote':
            s += '<blockquote>'
            for item in block.contents:
                s += '<p>' + item + '</p>'
            s += '</blockquote>'
        elif block.btype == 'ul':
            s += '<ul>'
            for item in block.contents:
                s += '<li>' + item + '</li>'
            s += '</ul>'
        elif block.btype == 'code':
            s += '<pre>' + '\n'.join(block.contents) + '</pre>'
        else:
            assert 0, 'unknow htmlblock type: {}'.format(block.btype)
    s += '</div></body></html>'
    return s


def global_symbol_conversion_on_html(s):
    """ change global symbol conversion on generated html draft
    ** ** -> strong
    * * -> i
    []() -> <a>
    ![]() -> <img>
    """
    s = re.sub(r'\*\*(?P<center>[^\*]+)\*\*', r'<strong>\g<center></strong>', s)
    s = re.sub(r'\*(?P<center>[^\*]+)\*', r'<i>\g<center></i>', s)
    s = re.sub(r'!\[(?P<imgtext>[^\[\]\"]+)\]((?P<url>[^\(\)\[\]\"]+))', r'<img src="\g<url>" alt="\g<imgtext>"/>', s)
    s = re.sub(r'\[(?P<urltext>[^\[\]\"]+)\]\((?P<url>[^\(\)\[\]]+)\)', r'<a href="\g<url>">\g<urltext></a>', s)
    s = re.sub(r'`(?P<text>[^`]+)`', r'<code>\g<text></code>', s)
    return s


if __name__ == '__main__':
    blog_title = '词向量和Word2Vec'
    update_time = 'time: {}'.format(time.strftime('%Y-%m-%d %H:%M:%S'))
    config = {
        "blog_title": blog_title,
        "create_time": update_time,
        "css_file": "common.css",
        "index_page": "index.html"
    }

    blocks = build_blocks_from_md_file('b.md')
    smoothed_blocks = smooth_blocks(blocks)
    html_draft = generate_html(smoothed_blocks, config)
    html_code = global_symbol_conversion_on_html(html_draft)
    with open('D:\\project\\oracle\\public\\blog\\nlp\\nlp-1-word2vec.html', 'w', encoding='utf8') as fout:
        fout.write(html_code)

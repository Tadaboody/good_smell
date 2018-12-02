from iter_lint import LintSmell
import re
import os

class RangeLenRGX(LintSmell):

    def check_for_smell(self) -> bool:
        return bool(re.search(self.source_code, r"for \w+ in range\(len\(.+\)\):"))

    def fix_smell(self) -> str:
        fixed_source = self.source_code.rstrip() + os.linesep
        for for_match in re.finditer(r"\n*(?<!#)( *|\t*)for (\w+) in range\(len\((.+)\)\):", self.source_code):
            indent, index, seq = for_match.groups()
            for_statement = indent + "for " + index + " in range(len(" + seq + ")):" + os.linesep
            content_rgx = indent + "for " + index + r" in range\(len\(" + seq + r"\)\):" + os.linesep + "((" + indent + r"(\s+).+" + os.linesep + ")*)"
            content = re.search(content_rgx, fixed_source).group(1)
            fixed_content = content.replace(seq + "[" + index + "]", "elm")
            fixed_content = "{}for {}, elm in enumerate({}):".format(indent, index, seq) + os.linesep + fixed_content
            fixed_source = fixed_source.replace(for_statement + content, fixed_content)
        return fixed_source

if __name__ == "__main__":
    source = """    for i in range(len(a)):""" + os.linesep + """        print(a[i])"""
    print(source)
    rlr = RangeLenRGX(source)
    print(rlr.fix_smell())

            
        
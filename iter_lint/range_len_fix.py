from iter_lint import LintSmell
import re
import os

class RangeLenSmell(LintSmell):

    def check_for_smell(self) -> bool:
        return bool(re.search(self.source_code, r"for \w+ in range\(len\(.+\)\):"))

    def fix_smell(self) -> str:
        fixed_source = self.source_code.rstrip() + os.linesep
        for for_match in re.finditer(r"(\s*)for (\w+) in range\(len\((.+)\)\):", self.source_code):
            indent = for_match.group(1)
            index = for_match.group(2)
            seq = for_match.group(3)
            content_rgx = indent + "for " + index + r" in range\(len\(" + seq + r"\)\):\n((" + indent + r"(\s).+\n)*)"
            print(content_rgx)
            print(fixed_source)
            content = re.search(content_rgx, fixed_source).group(1)
            print(content)
            fixed_content = re.sub(seq + "[" + index + "]", "elm", content)
            fixed_content = "{}for {}, elm in enumerate({}):\n".format(indent, index, seq) + fixed_content
            fixed_source = re.sub(fixed_content, content, fixed_source)
        return fixed_source

if __name__ == "__main__":
    source = """    for i in range(len(a)):\n        print(a[i])\n"""
    print(source)
    rlr = RangeLenRGX(source)
    print(rlr.fix_smell())

            
        
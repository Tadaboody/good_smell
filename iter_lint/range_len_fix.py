from iter_lint import LintSmell
import re
import os

class RangeLenSmell(LintSmell):

    def check_for_smell(self) -> bool:
        return bool(re.search(self.source_code, r"\n*( *|\t*)for (\w+) in range\(len\((.+)\)\):"))

    def fix_smell(self) -> str:
        fixed_source = self.source_code.rstrip() + os.linesep
        for for_match in re.finditer(r"(?=\n*|\r*)( *|\t*)for (\w+) in range\(len\((.+)\)\):", self.source_code):  # https://regex101.com/r/ib52OT/1
            indent, index, seq = for_match.groups()
            for_statement = indent + "for " + re.escape(index) + " in range(len(" + re.escape(seq) + ")):" + os.linesep
            content_rgx = indent + "for " + re.escape(index) + r" in range\(len\(" + re.escape(seq) + r"\)\):" + os.linesep + "((" + indent + r"(\s+).+" + os.linesep + ")*)"
            content = re.search(content_rgx, fixed_source).group(1)
            assign = re.search(r"([^\s]+)\s*=\s*(.*)(" + re.escape(seq) + r"\[" + re.escape(index) + r"\]" + r")(.*)", content)  # https://regex101.com/r/CnibMS/1
            elm = "elm"
            i = 1
            while re.search(elm, fixed_source):
                elm = "elm" + str(i)
            fixed_content = content
            if assign and assign.group(2).strip() == assign.group(4).strip() == "":
                elm = assign.group(1)
                fixed_content = content.replace(assign.group(0), "")
                fixed_content = os.linesep.join([line for line in fixed_content.splitlines() if line.strip() != ""])
            fixed_content = fixed_content.replace(seq + "[" + index + "]", elm)
            if fixed_content.strip() == "":
                fixed_content += indent + "    pass"
            fixed_content = "{}for {}, {} in enumerate({}):".format(indent, index, elm, seq) + os.linesep + fixed_content
            fixed_source = fixed_source.replace(for_statement + content, fixed_content + os.linesep)
        return (fixed_source).replace("\r", "")
            
        
# LSP : Linea Server Pages Language

import sys
import liblinea
from liblinea import LSP

def executeLSPCode(LSPCode):
    LSPCode = LSP.removeTagsFromLSPCode(LSPCode)
    if "Syntax Error" in LSPCode:
        return LSPCode  # Return error if tags are missing
    if "var" in LSPCode:
        if "=" in LSPCode:
            variable = LSPCode.split("=")[0].replace("var", "").strip()
            value = LSPCode.split("=")[1].strip()
            try:
                # Store the variable value as a string
                liblinea._lspVariables[variable] = value.strip('"').strip("'")
                return ""  # Return an empty string for successful variable declaration
            except:
                return "Syntax Error: Invalid value in variable declaration"
        else:
            return "Syntax Error: Missing '=' in variable declaration"
    elif "display" in LSPCode:
        displayParam = LSPCode.replace("display", "").strip()
        if displayParam.startswith('"') or displayParam.startswith("'"):
            if "+" in displayParam:
                result = LSP.breakPhraseToWords(displayParam, LSP._lspVariables)
                if isinstance(result, str) and result.startswith("Syntax Error"):
                    return result  # Return error if `breakPhraseToWords` fails
                return LSP.displayLSP(result)
            else:
                return LSP.displayLSP(displayParam[1:-1])
        else:
            if displayParam in LSP._lspVariables:
                return LSP.displayLSP(LSP._lspVariables[displayParam])
            elif displayParam.isdigit():
                return LSP.displayLSP(displayParam)
            else:
                return f"Syntax Error: Variable '{displayParam}' not found"
    elif LSPCode.startswith("web "):
        webParam = LSPCode.replace("web", "").strip()
        if webParam.startswith('"') or webParam.startswith("'"):
            return LSP.web(webParam[1:-1])
        else:
            return f"Syntax Error: Invalid web parameter '{webParam}'"
    elif LSPCode.startswith("evaluate "):
        expression = LSPCode.replace("evaluate", "").strip()
        result = LSP.evaluate(expression, LSP._lspVariables)
        if isinstance(result, str) and result.startswith("Syntax Error"):
            return result
    elif LSPCode.startswith("prompt "):
        prompt = LSPCode.replace("prompt", "").strip()
        return LSP.prompt(prompt)
    elif LSPCode.startswith("confirm "):
        confirm = LSPCode.replace("confirm", "").strip()
        return LSP.confirm(confirm)
    elif LSPCode.startswith("alert "):
        alert = LSPCode.replace("alert", "").strip()
        return LSP.alert(alert)
    else:
        return "Syntax Error: Invalid LSP code"
    

def main(file):
    with open(file, "r") as f:
        LSPCode = f.read()
        resCode = ""
        for line in LSPCode.split("\n"):
            if line.startswith("<?lsp") and line.endswith("?>"):
                result = executeLSPCode(line)
                if result is None:
                    result = ""  # Ensure result is a string
                resCode += result + "\n"
            else:
                resCode += line + "\n"
    return resCode
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: lsp.py <file>")
        sys.exit(1)
    print(main(sys.argv[1]))
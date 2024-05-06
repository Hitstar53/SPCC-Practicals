class ArgumentListArray:
    def __init__(self, index, arg):
        self.index = index
        self.arg = arg
        self.next = None


class DefinitionTable:
    def __init__(self, index, definition):
        self.index = index
        self.definition = definition
        self.arg = [None, None]
        self.next = None


class NameTable:
    def __init__(self, index, name):
        self.index = index
        self.name = name
        self.dt_index = None
        self.next = None


class MacroProcessor:
    def __init__(self):
        self.dt_head = None
        self.nt_head = None
        self.al_head = None
        self.al_index = 1
        self.MDTC = 1
        self.MNTC = 1

    def find_arg_index(self, arg):
        temp = self.al_head
        while temp is not None:
            if temp.arg == arg:
                return temp
            temp = temp.next
        return None

    def find_name(self, name):
        temp = self.nt_head
        while temp is not None:
            if temp.name == name:
                return temp.dt_index
            temp = temp.next
        return None

    def pass1(self, file_path):
        with open(file_path, "r") as fp:
            lines = fp.readlines()

        dt_temp = self.dt_head
        nt_temp = self.nt_head
        al_temp = self.al_head

        for line in lines:
            if "MACRO" in line:
                tokens = line.split()
                print(f"\nMACRO {tokens[0]} Detected...\n")

                if self.nt_head is None:
                    self.nt_head = NameTable(self.MNTC, tokens[0])
                    nt_temp = self.nt_head
                else:
                    nt_temp.next = NameTable(self.MNTC, tokens[0])
                    nt_temp = nt_temp.next

                self.MNTC += 1
                print(f"\n{tokens[0]} added into Name Table")

                for token in tokens[1:]:
                    if token != "MACRO" and token != "\n":
                        if self.al_head is None:
                            self.al_head = ArgumentListArray(self.al_index, token)
                            al_temp = self.al_head
                        else:
                            al_temp.next = ArgumentListArray(self.al_index, token)
                            al_temp = al_temp.next

                        self.al_index += 1
                        print(
                            f"\nArgument {al_temp.arg} added into argument list array"
                        )

                if self.dt_head is None:
                    self.dt_head = DefinitionTable(self.MDTC, nt_temp.name)
                    dt_temp = self.dt_head
                else:
                    dt_temp.next = DefinitionTable(self.MDTC, nt_temp.name)
                    dt_temp = dt_temp.next

                print(f"\nDefinition table entry created for {nt_temp.name}")
                nt_temp.dt_index = dt_temp

                for line in lines[lines.index(line) + 1 :]:
                    if line.strip() == "MEND":
                        break

                    tokens = line.split()
                    is_arg = 0
                    index = 0

                    for token in tokens:
                        if is_arg == 0:
                            dt_temp.next = DefinitionTable(self.MDTC, token)
                            dt_temp = dt_temp.next
                            self.MDTC += 1
                            print(
                                f"\nEntry appended for {dt_temp.definition} at index {dt_temp.index}"
                            )
                            is_arg = 1
                        else:
                            if self.find_arg_index(token) is None:
                                al_temp.next = ArgumentListArray(
                                    al_temp.index + 1, token
                                )
                                al_temp = al_temp.next
                                dt_temp.arg[index] = al_temp
                            else:
                                dt_temp.arg[index] = self.find_arg_index(token)
                            index += 1

        print("\nAll three tables are updated. Pass 1 Complete!\n")

    def pass2(self, file_path):
        with open(file_path, "r") as fp:
            lines = fp.readlines()

        with open("output.txt", "a") as ofp:
            for line in lines:
                print(f"\n{line}")
                temp = self.find_name(line.strip())

                if temp is not None:
                    while temp.definition != "MEND":
                        ofp.write(f"- {temp.definition} {temp.arg[0]} {temp.arg[1]}\n")
                        temp = temp.next

        print("\nOutput file updated with expanded code. Pass 2 Complete!\n")


if __name__ == "__main__":
    mp = MacroProcessor()
    print("\nPass 1 in progress\n")
    mp.pass1("./Exp9/input.asm")
    print("\nPass 2 in progress\n")
    mp.pass2("./Exp9/input.asm")

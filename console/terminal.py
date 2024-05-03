import os
import readchar

class Terminal:
    def __init__(self) -> None:
        self.env={"box":"","snap":""}
        self.history=[]
        self.commands = self.get_available_commands()

    def get_available_commands(self):
        terminal_path   = os.path.realpath(__file__)
        terminal_dir    = os.path.abspath(os.path.join(terminal_path,os.pardir))
        commands_dir    = os.path.join(terminal_dir,"commands")
        files           = [f for f in os.listdir(commands_dir) if os.path.isfile(os.path.join(commands_dir, f))]
        pyfiles         = [f for f in files if f.endswith(".py")]
        commands        = [f.split(".py")[0] for f in pyfiles]
        print(commands)

    def get_prompt(self):
        if self.env["box"]=="":return ">"
        if self.env["snap"]=="":return self.env["box"] + ">"
        return self.env["snap"] + "@" + self.env["box"] + ">"

    def run(self):
        os.system("clear")
        current_command = ""
        while True: # terminal Loop
            # Prepare to accept next command
            print("--> ",end="",flush=True)

            command = ""             
            while True: # command loop
                c = readchar.readchar()
                

                # ENTER : Send command
                if ord(c)==10:
                    current_command=command.strip()
                    print("\n",end="")
                    break

                # BACKSPACE : Erase command
                if ord(c)==127:
                    command = command[:-1]


                # VALID CHAR : Write command
                if c.isalnum() or c in ["-"," "]:command += c


                # Clear old line
                print("\r"+" "*(len(command)+10),end="")
                # Render new line
                print("\r-->",command,end="",flush=True)


            if current_command.lower() in ["quit","exit"]:break
            self.execute_command(current_command)


                

                 
            

    def execute_command(self,command):
        pass
        


# Run Instance
terminal = Terminal()
# terminal.run()



# str = ""
# while(1):
#     c = readchar.readchar()
#     print(ord(c),end="",flush=True)
#     if c=="\n":print("ENTER")
#     if c=="\t":print("TAB")
#     if c==" ":break
# print(str)



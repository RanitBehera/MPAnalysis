import os
import readchar
import commands

class Terminal:
    def __init__(self) -> None:
        self.env                = {}
        self.commands_history   = []

        # --- Initialise environment
        self.env["TERM_PATH"]   = os.path.realpath(__file__)
        self.env["TERM_DIR"]    = os.path.abspath(os.path.join(os.path.realpath(__file__),os.pardir))
        self.env["BOXBANK_DIR"] = os.path.join(self.env["TERM_DIR"],"registry/boxbank")
        self.env["BOX"]         = ""
        self.env["SNAP"]        = ""
        self.env["HALO"]        = ""

        # --- Get available executables
        self.exec_list          = []
        with open(os.path.join(self.env["TERM_DIR"],"registry/path.txt"))as f:
            paths = f.read().split("\n")
        for path in paths:
            self.exec_list += self.get_available_exec(path)

    def get_available_exec(self,exec_dir:str,recursive:bool=True):
        exec_list = []

        # Search others
        childs      = [c for c in os.listdir(exec_dir)]
        subfiles    = [f for f in childs if os.path.isfile(os.path.join(exec_dir, f))]
        subdirs     = [d for d in childs if os.path.isdir(os.path.join(exec_dir, d))]
        
        # Include files
        pyfiles     = [p for p in subfiles if p.endswith(".py") and not p.startswith(("_","__"))]
        for pyfile in pyfiles:
            exec_list.append(pyfile.split(".py")[0])

        # Include files from sub-folders
        if recursive:
            searchdirs = [os.path.join(exec_dir,d) for d in subdirs if not d.startswith((".","_","__"))]
            for sdir in searchdirs:
                sub_exec_list = self.get_available_exec(sdir)       # <--- Recursion
                exec_list += sub_exec_list

        return exec_list

    def get_prompt(self):
        if self.env["BOX"]=="":return "-->"
        if self.env["SNAP"]=="":return self.env["BOX"] + " -->"
        if self.env["HALO"]=="":return self.env["SNAP"] + " @ " + self.env["BOX"] + " -->"
        return self.env["SNAP"] + " @ " + self.env["BOX"] + " : " + self.env["HALO"] +" -->"

    def get_command(self):
        prev=-1
        floating_command = ""
        current_command = " "   
        # Space is important, empty will cause edgecase bug
        # Bug is basically you can't come to empty string terminal state due to logic


        while True: # command loop
            c = readchar.readkey()
            
            # ARROW : Navigate History
            if c==readchar.key.UP:
                if prev==-1:current_command = floating_command
                prev+=1
                if prev>len(self.commands_history)-1:prev = len(self.commands_history)-1
                floating_command = self.commands_history[prev]
            if c==readchar.key.DOWN:
                prev-=1
                if prev<-1:prev = -1

                if prev>-1:
                    floating_command = self.commands_history[prev]

                if prev==-1 and not current_command==" ": # Space is important, empty will cause edgecase bug
                    floating_command = current_command
                    current_command = " " # Space is important, empty will cause edgecase bug



            # ENTER : Send command
            if c==readchar.key.ENTER:
                print("\n",end="")
                break

            # BACKSPACE : Erase command
            if c==readchar.key.BACKSPACE:
                floating_command = floating_command[:-1]


            # VALID CHAR : Write command
            if c.isalnum() or c in ["-"," ","_","."]:floating_command += c


            # Clear old line
            print("\r"+" "*100,end="")
            # Render new line
            print("\r"+self.get_prompt(),floating_command,end="",flush=True)

        return floating_command.strip()



    def run(self):
        # Start with a fresh screen
        os.system("clear")
        
        command = ""
        while True:
            print(self.get_prompt(),end=" ",flush=True)
            command=self.get_command()
            
            # if current command is to exit, exit immediately
            if command.lower() in ["quit","exit"]:break

            # Update command history
            if command in self.commands_history:
                self.commands_history.remove(command)
            self.commands_history.insert(0,command)

            # Internal commands
            # ---
            if command.lower() in ["clear","cls","clc"]:os.system("clear");continue
            # ---

            # external commands
            self.execute_command(command)
            print("")

    def execute_command(self,command):
        command_chunks = command.split(" ")
        exec = command_chunks[0]

        if not exec in self.exec_list:
            print(f"Command '{exec}' not recognized.");return
        else:
            exec_args = command_chunks[1:]
            submodule = getattr(commands,exec)
            submodule.main(exec_args,self.env)




# -----------------------------------------------
t = Terminal()
print(t.exec_list)

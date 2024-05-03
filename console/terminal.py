import os
import readchar
import commands
import commands.box



class Terminal:
    def __init__(self) -> None:
        self.env                = {}
        self.commands_history   = []
        # --- Initialise environment
        self.env["TERM_PATH"]   = os.path.realpath(__file__)
        self.env["TERM_DIR"]    = os.path.abspath(os.path.join(os.path.realpath(__file__),os.pardir))
        self.env["EXEC_DIR"]    = os.path.join(self.env["TERM_DIR"],"commands")
        self.env["BOXBANK_DIR"]    = os.path.join(self.env["TERM_DIR"],"registry/boxbank")
        self.env["BOX"]         = ""
        self.env["SNAP"]        = ""
        self.env["HALO"]
        # --- Get available executables
        self.exec_list          = self.get_available_exec(self.env["EXEC_DIR"])

    def get_available_exec(self,exec_dir):
        files       = [f for f in os.listdir(exec_dir) if os.path.isfile(os.path.join(exec_dir, f))]
        pyfiles     = [f for f in files if f.endswith(".py")]
        exec_list   = [f.split(".py")[0] for f in pyfiles]
        return exec_list

    def get_prompt(self):
        if self.env["BOX"]=="":return "-->"
        if self.env["SNAP"]=="":return self.env["BOX"] + " -->"
        if self.env["HALO"]=="":return self.env["SNAP"] + "@" + self.env["BOX"] + " -->"
        return self.env["SNAP"] + "@" + self.env["BOX"] + ":" + self.env["HALO"] +" -->"

    def get_command(self):
        prev=-1
        floating_command = ""
        while True: # command loop
            c = readchar.readkey()
            
            # ARROW : Navigate History
            if c==readchar.key.UP:prev+=1
            if c==readchar.key.DOWN:prev-=1
            if prev>len(self.commands_history)-1:prev = len(self.commands_history)-1
            if prev<-1:prev = -1


            # ENTER : Send command
            if c==readchar.key.ENTER:
                print("\n",end="")
                break

            # BACKSPACE : Erase command
            if c==readchar.key.BACKSPACE:
                floating_command = floating_command[:-1]


            # VALID CHAR : Write command
            if c.isalnum() or c in ["-"," "]:floating_command += c
            
            # Display command
            display_command = ""

            if prev<0:display_command = floating_command
            else:display_command = self.commands_history[prev]

            # Clear old line
            print("\r"+" "*100,end="")
            # Render new line
            print("\r"+self.get_prompt(),display_command,end="",flush=True)

        if prev>-1:floating_command = self.commands_history[prev]

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
t.run()


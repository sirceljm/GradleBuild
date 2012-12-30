import sublime, sublime_plugin, sys, os
import subprocess
import re

def preparelist(l):
    new_list = []
    for x in l:
        x = x.strip().strip("\"").strip("'")
        if(x[0] != "_"):
            new_list.append(x)
    return new_list

class GradleBuildExecCommand(sublime_plugin.WindowCommand):
    def run(self, **kwargs):
        self.folder = ""
        self.buildScript = ""
        
        number_of_folders_in_project = len(self.window.folders())
        if number_of_folders_in_project > 1:
            print "There are more than one folders in project. Only the first \"gradle.build\" script found will be used!"
        if len(self.window.folders()) > 0:
            for folder in self.window.folders():
                if os.path.exists(folder + os.sep + "build.gradle"):
                    self.folder = folder
                    self.buildScript = folder + os.sep + "build.gradle";
                    break

        if self.buildScript == "":
            print "Could not find build script!"
            return

        print self.buildScript

        try:
            f = open(self.buildScript);
        except Exception as ex:
            print ex;
            return 'The file could not be opened'
    
        data = f.read();
        self.tasks = re.findall(r"task(.*?)\<\<", data, re.DOTALL|re.MULTILINE)
        self.tasks = preparelist(self.tasks)

        self.tasks = sorted(self.tasks);

        previousTask = None
        count = 0
        for task in self.tasks:
            if previousTask == None:
                previousTask = task[0]
            elif task[0] != "#" and previousTask != task[0]:
                self.tasks.insert(count, "#############################################")
                previousTask = task[0]
            count = count + 1

        self.window.show_quick_panel(self.tasks, self._quick_panel_callback);
    def _quick_panel_callback(self, index):
        if (index > -1):
            taskName = self.tasks[index];
            if taskName[0] != "#":
            
                gradle = "gradle";
                
                if sys.platform.startswith('win32'):
                        gradle = "gradle.bat";

                # TODO this is only for windows
                print self.folder
                p = subprocess.Popen(["cmd", "/K", "cd", self.folder, "&&", gradle, "-q", taskName])


                


                


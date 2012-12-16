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
        
        package_dir = os.path.join(sublime.packages_path(), "GradleBuild");

        try:
            f = open(folder + os.sep + "build.gradle");
        except Exception as ex:
            print ex;
            return 'File "build.gradle" could not be found'
    
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
                # Check for Windows Overrides and Merge
                if sys.platform.startswith('win32'):
                        gradle = "gradle.bat";

                # TODO this is only for windows
                p = subprocess.Popen(["cmd", "/K", gradle, "-q", taskName])


                


                


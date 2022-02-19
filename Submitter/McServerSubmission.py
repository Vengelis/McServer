"""
 Created by Vengelis_.
 Date: 2/19/2022
 Time: 1:28 AM
 Project: McServer
"""

from System import *
from System.Collections.Specialized import *
from System.IO import *
from System.Text import *

from Deadline.Scripting import *
from DeadlineUI.Controls.Scripting.DeadlineScriptDialog import DeadlineScriptDialog

# Job Options UI
import imp
import os

imp.load_source("JobOptionsUI", os.path.join(RepositoryUtils.GetRepositoryPath("submission/Common/Main", True), "JobOptionsUI.py"))
import JobOptionsUI

########################################################################
## Globals
########################################################################
scriptDialog = None
settings = None
count = 0
jobOptions_dialog = None


########################################################################
## Main Function Called By Deadline
########################################################################
def __main__(*args):
    global scriptDialog
    global settings
    global CommandBox
    global jobOptions_dialog

    scriptDialog = DeadlineScriptDialog()
    scriptDialog.SetTitle("Submit Minecraft Server Job To Deadline - v1.0")
    scriptDialog.SetIcon(scriptDialog.GetIcon('McServer'))

    jobOptions_dialog = JobOptionsUI.JobOptionsDialog(parentAppName="McServerMonitor")

    scriptDialog.AddScriptControl("JobOptionsDialog", jobOptions_dialog, "")

    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid("Separator3", "SeparatorControl", "Minecraft Server Options", 0, 0, colSpan=5)

    scriptDialog.AddControlToGrid("JobTypeLabel", "LabelControl", "Job Type", 1, 0, "Choose a normal or maintenance job.", False)
    jobTypeBox = scriptDialog.AddComboControlToGrid("JobTypeBox", "ComboControl", "Normal", ("Normal", "Development"), 1, 1)
    jobTypeBox.ValueModified.connect(jobTypeChanged)

    scriptDialog.AddControlToGrid("CommandsLabel", "LabelControl", "Launchers to Execute: 0", 2, 0, "Specify a list of commands to execute, one commmand per line.", colSpan=6)

    InsertFileButton = scriptDialog.AddControlToGrid("InsertFileButton", "ButtonControl", "Insert File Path", 3, 0, "Insert a file path at the current cursor location.", False)
    InsertFileButton.ValueModified.connect(InsertFilePressed)

    InsertFolderButton = scriptDialog.AddControlToGrid("InsertFolderButton", "ButtonControl", "Insert Folder Path", 3, 1, "Insert a folder path at the current cursor location.", False)
    InsertFolderButton.ValueModified.connect(InsertFolderPressed)

    LoadButton = scriptDialog.AddControlToGrid("LoadButton", "ButtonControl", "Load", 3, 3, tooltip="Load a list of commands from a file.", expand=False)
    LoadButton.ValueModified.connect(LoadPressed)

    SaveButton = scriptDialog.AddControlToGrid("SaveButton", "ButtonControl", "Save", 3, 4, tooltip="Save the current list of commands to a file.", expand=False)
    SaveButton.ValueModified.connect(SavePressed)

    ClearButton = scriptDialog.AddControlToGrid("ClearButton", "ButtonControl", "Clear", 3, 5, tooltip="Clear the current list of commands.", expand=False)
    ClearButton.ValueModified.connect(ClearPressed)

    CommandBox = scriptDialog.AddControlToGrid("CommandsBox", "MultiLineTextControl", "", 4, 0, colSpan=6)
    CommandBox.ValueModified.connect(CommandsChanged)

    scriptDialog.AddControlToGrid("StartupLabel", "LabelControl", "Startup Directory", 5, 0, "The directory where each command will startup (optional).", False)
    scriptDialog.AddSelectionControlToGrid("StartupBox", "FolderBrowserControl", "", "", 5, 1, colSpan=3)

    shellExecute = scriptDialog.AddSelectionControlToGrid("ShellExecuteBox", "CheckBoxControl", False, "Execute In Shell", 6, 0, "If enabled, the specified argument(s) will be executed through the current shell.")
    shellExecute.ValueModified.connect(ShellExecuteButtonPressed)
    scriptDialog.AddComboControlToGrid("ShellToUseBox", "ComboControl", "default", ["default", "bash", "sh", "cmd"], 6, 1)
    scriptDialog.AddHorizontalSpacerToGrid("HSpacer1", 7, 0)
    scriptDialog.EndGrid()

    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid("Separator3", "SeparatorControl", "UWA Generator Options", 0, 0, colSpan=5)

    uwaEnabledExecute = scriptDialog.AddSelectionControlToGrid("UwaEnabledExecuteBox", "CheckBoxControl", False, "UWA Enabled", 1, 0, "If enabled, UWA was setuped")
    uwaEnabledExecute.ValueModified.connect(UwaEnabledExecuteButtonPressed)

    uwaStandaloneServerExecute = scriptDialog.AddSelectionControlToGrid("UwaStandaloneServerExecuteExecuteBox", "CheckBoxControl", False, "Standalone Generator Server", 1, 3, "If enabled, is standalone server")
    uwaStandaloneServerExecute.ValueModified.connect(UwaSSSExecuteButtonPressed)

    uwaRegenExecute = scriptDialog.AddSelectionControlToGrid("UwaRegenExecuteBox", "CheckBoxControl", False, "Regen MAP", 2, 0, "If enabled, Uwa regen the current map")
    # uwaRegenExecute.ValueModified.connect(UwaExecuteButtonPressed)

    scriptDialog.AddControlToGrid("UwaGeneratorMapNumberPerTaskLabel", "LabelControl", "Map per task", 2, 3, "Number of map per task to generate", False)
    scriptDialog.AddRangeControlToGrid("UwaGeneratorMapNumberPerTaskBox", "RangeControl", 1, 1, 1000, 0, 1, 2, 4, expand=False)

    uwaPregenExecute = scriptDialog.AddSelectionControlToGrid("UwaPregenExecuteBox", "CheckBoxControl", False, "Pregen MAP", 3, 0, "If enabled, UWA pregen the current map")
    uwaPregenExecute.ValueModified.connect(UwaPregenExecuteButtonPressed)

    scriptDialog.AddControlToGrid("UwaGeneratorMapNumberLabel", "LabelControl", "Task number", 3, 3, "Number of task in the job", False)
    scriptDialog.AddRangeControlToGrid("UwaGeneratorMapNumberBox", "RangeControl", 1, 1, 1000, 0, 1, 3, 4, expand=False)

    scriptDialog.AddControlToGrid("UwaPregenerateChunkLabel", "LabelControl", "Pregen Radius Chunk", 4, 0, "Radius of pregen generator", False)
    scriptDialog.AddRangeControlToGrid("UwaPregenerateChunkBox", "RangeControl", 1, 500, 10000, 0, 50, 4, 1, expand=False)

    scriptDialog.AddControlToGrid("UwaGeneratorMapTypeLabel", "LabelControl", "Map Type", 4, 3, "Type of map to generate", False)
    scriptDialog.AddComboControlToGrid("UwaUhcTypeGeneratorToUseBox", "ComboControl", "all types", ["uhc", "lg", "all types"], 4, 4)

    scriptDialog.AddControlToGrid("UwaGenerateMapTypeLabel", "LabelControl", "Map Type", 5, 0, "Type of map to load", False)
    scriptDialog.AddComboControlToGrid("UwaUhcTypeToUseBox", "ComboControl", "default", ["default", "uhc", "lg", "random"], 5, 1)

    scriptDialog.EndGrid()

    scriptDialog.AddGrid()
    scriptDialog.AddHorizontalSpacerToGrid("HSpacer2", 0, 0)
    submitButton = scriptDialog.AddControlToGrid("SubmitButton", "ButtonControl", "Submit", 1, 1, expand=False)
    submitButton.ValueModified.connect(SubmitButtonPressed)

    closeButton = scriptDialog.AddControlToGrid("CloseButton", "ButtonControl", "Close", 1, 2, expand=False)
    closeButton.ValueModified.connect(scriptDialog.closeEvent)
    closeButton.ValueModified.connect(jobOptions_dialog.closeEvent)
    scriptDialog.EndGrid()

    settings = ("ChunkSizeBox", "StartupBox", "ShellExecuteBox", "ShellToUseBox")
    scriptDialog.LoadSettings(GetSettingsFilename(), settings)
    scriptDialog.EnabledStickySaving(settings, GetSettingsFilename())

    jobTypeChanged(None)
    ShellExecuteButtonPressed(None)
    UwaEnabledExecuteButtonPressed(None)
    UwaSSSExecuteButtonPressed(None)
    UwaPregenExecuteButtonPressed(None)

    scriptDialog.ShowDialog(True)


def jobTypeChanged(*args):
    global scriptDialog

    normalJob = scriptDialog.GetValue("JobTypeBox")


def CommandsChanged(self):
    global count
    count = 0

    for line in scriptDialog.GetItems("CommandsBox"):
        if (len(line) > 0):
            count += 1
        else:
            # This is since we can't have blank lines between commands
            break

    scriptDialog.SetValue("CommandsLabel", "Commands to Execute: " + str(count))


def InsertFilePressed(self):
    global scriptDialog

    selection = scriptDialog.ShowOpenFileBrowser("", "All Files (*)")
    if selection != None:
        selection = ("\"%s\"" % selection)
        CommandBox.insertPlainText(selection)


def InsertFolderPressed(self):
    global scriptDialog

    selection = scriptDialog.ShowFolderBrowser("")
    if selection != None:
        selection = ("\"%s\"" % selection)
        CommandBox.insertPlainText(selection)


def LoadPressed(self):
    global scriptDialog

    selection = scriptDialog.ShowOpenFileBrowser("", "All Files (*)")
    if selection != None:
        file = open(selection, "r")

        # This gets rid of square characters in the text box
        text = file.read().replace("\r\n", "\n")
        scriptDialog.SetItems("CommandsBox", tuple(text.split("\n")))

        file.close()


def SavePressed(self):
    global scriptDialog

    selection = scriptDialog.ShowSaveFileBrowser("", "All Files (*)")
    if selection != None:
        file = open(selection, "w")

        for line in scriptDialog.GetItems("CommandsBox"):
            if len(line) > 0:
                file.write(line + "\n")
            else:
                # This is since we can't have blank lines between commands
                break

        file.close()


def ClearPressed(self):
    global scriptDialog
    scriptDialog.SetValue("CommandsBox", "")
    scriptDialog.SetValue("CommandsLabel", "Commands to Execute: 0")


def GetSettingsFilename():
    return Path.Combine(ClientUtils.GetUsersSettingsDirectory(), "CommandScriptSettings.ini")


def ShellExecuteButtonPressed(*args):
    global scriptDialog
    state = scriptDialog.GetValue("ShellExecuteBox")
    scriptDialog.SetEnabled("ShellToUseBox", state)


def UwaEnabledExecuteButtonPressed(*args):
    global scriptDialog
    state = scriptDialog.GetValue("UwaEnabledExecuteBox")
    scriptDialog.SetEnabled("UwaStandaloneServerExecuteExecuteBox", not state)
    scriptDialog.SetEnabled("UwaRegenExecuteBox", state)
    scriptDialog.SetEnabled("UwaPregenExecuteBox", state)
    scriptDialog.SetEnabled("UwaPregenerateChunkLabel", state)
    scriptDialog.SetEnabled("UwaPregenerateChunkBox", state)
    scriptDialog.SetEnabled("UwaGenerateMapTypeLabel", state)
    scriptDialog.SetEnabled("UwaUhcTypeToUseBox", state)
    UwaPregenExecuteButtonPressed(None)


def UwaSSSExecuteButtonPressed(*args):
    global scriptDialog
    state = scriptDialog.GetValue("UwaStandaloneServerExecuteExecuteBox")
    scriptDialog.SetEnabled("UwaEnabledExecuteBox", not state)
    scriptDialog.SetEnabled("UwaGeneratorMapNumberPerTaskLabel", state)
    scriptDialog.SetEnabled("UwaGeneratorMapNumberPerTaskBox", state)
    scriptDialog.SetEnabled("UwaGeneratorMapNumberLabel", state)
    scriptDialog.SetEnabled("UwaGeneratorMapNumberBox", state)
    scriptDialog.SetEnabled("UwaGeneratorMapTypeLabel", state)
    scriptDialog.SetEnabled("UwaUhcTypeGeneratorToUseBox", state)


def UwaPregenExecuteButtonPressed(*args):
    global scriptDialog
    state = scriptDialog.GetValue("UwaPregenExecuteBox")
    scriptDialog.SetEnabled("UwaPregenerateChunkLabel", state)
    scriptDialog.SetEnabled("UwaPregenerateChunkBox", state)


def SubmitButtonPressed(*args):
    global scriptDialog
    global count
    global jobOptions_dialog

    errors = []

    CommandsChanged(None)

    if (count == 0):
        errors.append("The command list is empty!")

    if len(errors) > 0:
        scriptDialog.ShowMessageBox("The following errors were encountered:\n\n%s\n\nPlease resolve these issues and submit again.\n" % ("\n\n".join(errors)), "Errors")
        return

    jobOptions = jobOptions_dialog.GetJobOptionsValues()

    # Create job info file.
    jobInfoFilename = Path.Combine(ClientUtils.GetDeadlineTempPath(), "mcserver3_job_info.job")
    writer = StreamWriter(jobInfoFilename, False, Encoding.Unicode)
    writer.WriteLine("Plugin=McServer")

    for option, value in jobOptions.iteritems():
        writer.WriteLine("%s=%s" % (option, value))

    writer.WriteLine("Frames=0-" + str(count * scriptDialog.GetValue("UwaGeneratorMapNumberBox") * scriptDialog.GetValue("UwaGeneratorMapNumberPerTaskBox") - 1))
    writer.WriteLine("ChunkSize=%s" % scriptDialog.GetValue("UwaGeneratorMapNumberPerTaskBox"))

    writer.Close()

    # Create plugin info file.
    pluginInfoFilename = Path.Combine(ClientUtils.GetDeadlineTempPath(), "mcserver3_plugin_info.job")
    writer = StreamWriter(pluginInfoFilename, False, Encoding.Unicode)

    writer.WriteLine("StartupDirectory=%s" % scriptDialog.GetValue("StartupBox").strip())
    writer.WriteLine("ShellExecute=%s" % scriptDialog.GetValue("ShellExecuteBox"))
    writer.WriteLine("Shell=%s" % scriptDialog.GetValue("ShellToUseBox"))

    if scriptDialog.GetValue("UwaEnabledExecuteBox"):
        writer.WriteLine("UwaStandaloneGenerator=%s" % False)
        writer.WriteLine("UwaEnabledExecuteBox=%s" % True)
        writer.WriteLine("UwaRegenExecuteBox=%s" % scriptDialog.GetValue("UwaRegenExecuteBox"))
        writer.WriteLine("UwaPregenExecuteBox=%s" % scriptDialog.GetValue("UwaPregenExecuteBox"))
        writer.WriteLine("UwaPregenerateChunkBox=%s" % scriptDialog.GetValue("UwaPregenerateChunkBox"))
        writer.WriteLine("UwaUhcTypeToUseBox=%s" % scriptDialog.GetValue("UwaUhcTypeToUseBox"))

    elif scriptDialog.GetValue("UwaStandaloneServerExecuteExecuteBox"):
        writer.WriteLine("UwaEnabledExecuteBox=%s" % False)
        writer.WriteLine("UwaStandaloneServerExecuteExecuteBox=%s" % True)
        writer.WriteLine("UwaGeneratorMapNumberPerTaskBox=%s" % scriptDialog.GetValue("UwaGeneratorMapNumberPerTaskBox"))
        writer.WriteLine("UwaGeneratorMapNumberBox=%s" % scriptDialog.GetValue("UwaGeneratorMapNumberBox"))
        writer.WriteLine("UwaUhcTypeGeneratorToUseBox=%s" % scriptDialog.GetValue("UwaUhcTypeGeneratorToUseBox"))

    else:
        writer.WriteLine("UwaEnabledExecuteBox=%s" % False)
        writer.WriteLine("UwaStandaloneServerExecuteExecuteBox=%s" % False)

    writer.Close()

    commandsFilename = Path.Combine(ClientUtils.GetDeadlineTempPath(), "commandsfile.txt")
    writer = StreamWriter(commandsFilename, False, Encoding.Unicode)

    for x in range(scriptDialog.GetValue("UwaGeneratorMapNumberBox")):
        for line in scriptDialog.GetItems("CommandsBox"):
            if len(line) > 0:
                writer.WriteLine(line)
            else:
                # This is since we can't have blank lines between commands
                break

    writer.Close()

    # Setup the command line arguments.
    arguments = StringCollection()

    arguments.Add(jobInfoFilename)
    arguments.Add(pluginInfoFilename)
    arguments.Add(commandsFilename)

    results = ClientUtils.ExecuteCommandAndGetOutput(arguments)
    scriptDialog.ShowMessageBox(results, "Submission Results")


from System import *
from System.Collections.Specialized import *
from System.IO import *
from System.Text import *

from Deadline.Scripting import *
from DeadlineUI.Controls.Scripting.DeadlineScriptDialog import DeadlineScriptDialog

# Job Options UI
import imp
import os

imp.load_source("JobOptionsUI", os.path.join(RepositoryUtils.GetRepositoryPath("submission/Common/Main", True), "JobOptionsUI.py"))
import JobOptionsUI

########################################################################
## Globals
########################################################################
scriptDialog = None
settings = None
count = 0
jobOptions_dialog = None


########################################################################
## Main Function Called By Deadline
########################################################################
def __main__(*args):
    global scriptDialog
    global settings
    global CommandBox
    global jobOptions_dialog

    scriptDialog = DeadlineScriptDialog()
    scriptDialog.SetTitle("Submit Minecraft Server Job To Deadline - v1.0")
    scriptDialog.SetIcon(scriptDialog.GetIcon('McServer'))

    jobOptions_dialog = JobOptionsUI.JobOptionsDialog(parentAppName="McServerMonitor")

    scriptDialog.AddScriptControl("JobOptionsDialog", jobOptions_dialog, "")

    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid("Separator3", "SeparatorControl", "Minecraft Server Options", 0, 0, colSpan=5)

    scriptDialog.AddControlToGrid("JobTypeLabel", "LabelControl", "Job Type", 1, 0, "Choose a normal or maintenance job.", False)
    jobTypeBox = scriptDialog.AddComboControlToGrid("JobTypeBox", "ComboControl", "Normal", ("Normal", "Development"), 1, 1)
    jobTypeBox.ValueModified.connect(jobTypeChanged)

    scriptDialog.AddControlToGrid("CommandsLabel", "LabelControl", "Launchers to Execute: 0", 2, 0, "Specify a list of commands to execute, one commmand per line.", colSpan=6)

    InsertFileButton = scriptDialog.AddControlToGrid("InsertFileButton", "ButtonControl", "Insert File Path", 3, 0, "Insert a file path at the current cursor location.", False)
    InsertFileButton.ValueModified.connect(InsertFilePressed)

    InsertFolderButton = scriptDialog.AddControlToGrid("InsertFolderButton", "ButtonControl", "Insert Folder Path", 3, 1, "Insert a folder path at the current cursor location.", False)
    InsertFolderButton.ValueModified.connect(InsertFolderPressed)

    LoadButton = scriptDialog.AddControlToGrid("LoadButton", "ButtonControl", "Load", 3, 3, tooltip="Load a list of commands from a file.", expand=False)
    LoadButton.ValueModified.connect(LoadPressed)

    SaveButton = scriptDialog.AddControlToGrid("SaveButton", "ButtonControl", "Save", 3, 4, tooltip="Save the current list of commands to a file.", expand=False)
    SaveButton.ValueModified.connect(SavePressed)

    ClearButton = scriptDialog.AddControlToGrid("ClearButton", "ButtonControl", "Clear", 3, 5, tooltip="Clear the current list of commands.", expand=False)
    ClearButton.ValueModified.connect(ClearPressed)

    CommandBox = scriptDialog.AddControlToGrid("CommandsBox", "MultiLineTextControl", "", 4, 0, colSpan=6)
    CommandBox.ValueModified.connect(CommandsChanged)

    scriptDialog.AddControlToGrid("StartupLabel", "LabelControl", "Startup Directory", 5, 0, "The directory where each command will startup (optional).", False)
    scriptDialog.AddSelectionControlToGrid("StartupBox", "FolderBrowserControl", "", "", 5, 1, colSpan=3)

    shellExecute = scriptDialog.AddSelectionControlToGrid("ShellExecuteBox", "CheckBoxControl", False, "Execute In Shell", 6, 0, "If enabled, the specified argument(s) will be executed through the current shell.")
    shellExecute.ValueModified.connect(ShellExecuteButtonPressed)
    scriptDialog.AddComboControlToGrid("ShellToUseBox", "ComboControl", "default", ["default", "bash", "sh", "cmd"], 6, 1)
    scriptDialog.AddHorizontalSpacerToGrid("HSpacer1", 7, 0)
    scriptDialog.EndGrid()

    scriptDialog.AddGrid()
    scriptDialog.AddControlToGrid("Separator3", "SeparatorControl", "UWA Generator Options", 0, 0, colSpan=5)

    uwaEnabledExecute = scriptDialog.AddSelectionControlToGrid("UwaEnabledExecuteBox", "CheckBoxControl", False, "UWA Enabled", 1, 0, "If enabled, UWA was setuped")
    uwaEnabledExecute.ValueModified.connect(UwaEnabledExecuteButtonPressed)

    uwaStandaloneServerExecute = scriptDialog.AddSelectionControlToGrid("UwaStandaloneServerExecuteExecuteBox", "CheckBoxControl", False, "Standalone Generator Server", 1, 3, "If enabled, is standalone server")
    uwaStandaloneServerExecute.ValueModified.connect(UwaSSSExecuteButtonPressed)

    uwaRegenExecute = scriptDialog.AddSelectionControlToGrid("UwaRegenExecuteBox", "CheckBoxControl", False, "Regen MAP", 2, 0, "If enabled, Uwa regen the current map")
    # uwaRegenExecute.ValueModified.connect(UwaExecuteButtonPressed)

    scriptDialog.AddControlToGrid("UwaGeneratorMapNumberPerTaskLabel", "LabelControl", "Map per task", 2, 3, "Number of map per task to generate", False)
    scriptDialog.AddRangeControlToGrid("UwaGeneratorMapNumberPerTaskBox", "RangeControl", 1, 1, 1000, 0, 1, 2, 4, expand=False)

    uwaPregenExecute = scriptDialog.AddSelectionControlToGrid("UwaPregenExecuteBox", "CheckBoxControl", False, "Pregen MAP", 3, 0, "If enabled, UWA pregen the current map")
    uwaPregenExecute.ValueModified.connect(UwaPregenExecuteButtonPressed)

    scriptDialog.AddControlToGrid("UwaGeneratorMapNumberLabel", "LabelControl", "Task number", 3, 3, "Number of task in the job", False)
    scriptDialog.AddRangeControlToGrid("UwaGeneratorMapNumberBox", "RangeControl", 1, 1, 1000, 0, 1, 3, 4, expand=False)

    scriptDialog.AddControlToGrid("UwaPregenerateChunkLabel", "LabelControl", "Pregen Radius Chunk", 4, 0, "Radius of pregen generator", False)
    scriptDialog.AddRangeControlToGrid("UwaPregenerateChunkBox", "RangeControl", 1, 500, 10000, 0, 50, 4, 1, expand=False)

    scriptDialog.AddControlToGrid("UwaGeneratorMapTypeLabel", "LabelControl", "Map Type", 4, 3, "Type of map to generate", False)
    scriptDialog.AddComboControlToGrid("UwaUhcTypeGeneratorToUseBox", "ComboControl", "all types", ["uhc", "lg", "all types"], 4, 4)

    scriptDialog.AddControlToGrid("UwaGenerateMapTypeLabel", "LabelControl", "Map Type", 5, 0, "Type of map to load", False)
    scriptDialog.AddComboControlToGrid("UwaUhcTypeToUseBox", "ComboControl", "default", ["default", "uhc", "lg", "random"], 5, 1)

    scriptDialog.EndGrid()

    scriptDialog.AddGrid()
    scriptDialog.AddHorizontalSpacerToGrid("HSpacer2", 0, 0)
    submitButton = scriptDialog.AddControlToGrid("SubmitButton", "ButtonControl", "Submit", 1, 1, expand=False)
    submitButton.ValueModified.connect(SubmitButtonPressed)

    closeButton = scriptDialog.AddControlToGrid("CloseButton", "ButtonControl", "Close", 1, 2, expand=False)
    closeButton.ValueModified.connect(scriptDialog.closeEvent)
    closeButton.ValueModified.connect(jobOptions_dialog.closeEvent)
    scriptDialog.EndGrid()

    settings = ("ChunkSizeBox", "StartupBox", "ShellExecuteBox", "ShellToUseBox")
    scriptDialog.LoadSettings(GetSettingsFilename(), settings)
    scriptDialog.EnabledStickySaving(settings, GetSettingsFilename())

    jobTypeChanged(None)
    ShellExecuteButtonPressed(None)
    UwaEnabledExecuteButtonPressed(None)
    UwaSSSExecuteButtonPressed(None)
    UwaPregenExecuteButtonPressed(None)

    scriptDialog.ShowDialog(True)


def jobTypeChanged(*args):
    global scriptDialog

    normalJob = scriptDialog.GetValue("JobTypeBox")


def CommandsChanged(self):
    global count
    count = 0

    for line in scriptDialog.GetItems("CommandsBox"):
        if (len(line) > 0):
            count += 1
        else:
            # This is since we can't have blank lines between commands
            break

    scriptDialog.SetValue("CommandsLabel", "Commands to Execute: " + str(count))


def InsertFilePressed(self):
    global scriptDialog

    selection = scriptDialog.ShowOpenFileBrowser("", "All Files (*)")
    if selection != None:
        selection = ("\"%s\"" % selection)
        CommandBox.insertPlainText(selection)


def InsertFolderPressed(self):
    global scriptDialog

    selection = scriptDialog.ShowFolderBrowser("")
    if selection != None:
        selection = ("\"%s\"" % selection)
        CommandBox.insertPlainText(selection)


def LoadPressed(self):
    global scriptDialog

    selection = scriptDialog.ShowOpenFileBrowser("", "All Files (*)")
    if selection != None:
        file = open(selection, "r")

        # This gets rid of square characters in the text box
        text = file.read().replace("\r\n", "\n")
        scriptDialog.SetItems("CommandsBox", tuple(text.split("\n")))

        file.close()


def SavePressed(self):
    global scriptDialog

    selection = scriptDialog.ShowSaveFileBrowser("", "All Files (*)")
    if selection != None:
        file = open(selection, "w")

        for line in scriptDialog.GetItems("CommandsBox"):
            if len(line) > 0:
                file.write(line + "\n")
            else:
                # This is since we can't have blank lines between commands
                break

        file.close()


def ClearPressed(self):
    global scriptDialog
    scriptDialog.SetValue("CommandsBox", "")
    scriptDialog.SetValue("CommandsLabel", "Commands to Execute: 0")


def GetSettingsFilename():
    return Path.Combine(ClientUtils.GetUsersSettingsDirectory(), "CommandScriptSettings.ini")


def ShellExecuteButtonPressed(*args):
    global scriptDialog
    state = scriptDialog.GetValue("ShellExecuteBox")
    scriptDialog.SetEnabled("ShellToUseBox", state)


def UwaEnabledExecuteButtonPressed(*args):
    global scriptDialog
    state = scriptDialog.GetValue("UwaEnabledExecuteBox")
    scriptDialog.SetEnabled("UwaStandaloneServerExecuteExecuteBox", not state)
    scriptDialog.SetEnabled("UwaRegenExecuteBox", state)
    scriptDialog.SetEnabled("UwaPregenExecuteBox", state)
    scriptDialog.SetEnabled("UwaPregenerateChunkLabel", state)
    scriptDialog.SetEnabled("UwaPregenerateChunkBox", state)
    scriptDialog.SetEnabled("UwaGenerateMapTypeLabel", state)
    scriptDialog.SetEnabled("UwaUhcTypeToUseBox", state)
    UwaPregenExecuteButtonPressed(None)


def UwaSSSExecuteButtonPressed(*args):
    global scriptDialog
    state = scriptDialog.GetValue("UwaStandaloneServerExecuteExecuteBox")
    scriptDialog.SetEnabled("UwaEnabledExecuteBox", not state)
    scriptDialog.SetEnabled("UwaGeneratorMapNumberPerTaskLabel", state)
    scriptDialog.SetEnabled("UwaGeneratorMapNumberPerTaskBox", state)
    scriptDialog.SetEnabled("UwaGeneratorMapNumberLabel", state)
    scriptDialog.SetEnabled("UwaGeneratorMapNumberBox", state)
    scriptDialog.SetEnabled("UwaGeneratorMapTypeLabel", state)
    scriptDialog.SetEnabled("UwaUhcTypeGeneratorToUseBox", state)


def UwaPregenExecuteButtonPressed(*args):
    global scriptDialog
    state = scriptDialog.GetValue("UwaPregenExecuteBox")
    scriptDialog.SetEnabled("UwaPregenerateChunkLabel", state)
    scriptDialog.SetEnabled("UwaPregenerateChunkBox", state)


def SubmitButtonPressed(*args):
    global scriptDialog
    global count
    global jobOptions_dialog

    errors = []

    CommandsChanged(None)

    if (count == 0):
        errors.append("The command list is empty!")

    if len(errors) > 0:
        scriptDialog.ShowMessageBox("The following errors were encountered:\n\n%s\n\nPlease resolve these issues and submit again.\n" % ("\n\n".join(errors)), "Errors")
        return

    jobOptions = jobOptions_dialog.GetJobOptionsValues()

    # Create job info file.
    jobInfoFilename = Path.Combine(ClientUtils.GetDeadlineTempPath(), "mcserver3_job_info.job")
    writer = StreamWriter(jobInfoFilename, False, Encoding.Unicode)
    writer.WriteLine("Plugin=McServer")

    for option, value in jobOptions.iteritems():
        writer.WriteLine("%s=%s" % (option, value))

    writer.WriteLine("Frames=0-" + str(count * scriptDialog.GetValue("UwaGeneratorMapNumberBox") * scriptDialog.GetValue("UwaGeneratorMapNumberPerTaskBox") - 1))
    writer.WriteLine("ChunkSize=%s" % scriptDialog.GetValue("UwaGeneratorMapNumberPerTaskBox"))

    writer.Close()

    # Create plugin info file.
    pluginInfoFilename = Path.Combine(ClientUtils.GetDeadlineTempPath(), "mcserver3_plugin_info.job")
    writer = StreamWriter(pluginInfoFilename, False, Encoding.Unicode)

    writer.WriteLine("StartupDirectory=%s" % scriptDialog.GetValue("StartupBox").strip())
    writer.WriteLine("ShellExecute=%s" % scriptDialog.GetValue("ShellExecuteBox"))
    writer.WriteLine("Shell=%s" % scriptDialog.GetValue("ShellToUseBox"))

    if scriptDialog.GetValue("UwaEnabledExecuteBox"):
        writer.WriteLine("UwaStandaloneGenerator=%s" % False)
        writer.WriteLine("UwaEnabledExecuteBox=%s" % True)
        writer.WriteLine("UwaRegenExecuteBox=%s" % scriptDialog.GetValue("UwaRegenExecuteBox"))
        writer.WriteLine("UwaPregenExecuteBox=%s" % scriptDialog.GetValue("UwaPregenExecuteBox"))
        writer.WriteLine("UwaPregenerateChunkBox=%s" % scriptDialog.GetValue("UwaPregenerateChunkBox"))
        writer.WriteLine("UwaUhcTypeToUseBox=%s" % scriptDialog.GetValue("UwaUhcTypeToUseBox"))

    elif scriptDialog.GetValue("UwaStandaloneServerExecuteExecuteBox"):
        writer.WriteLine("UwaEnabledExecuteBox=%s" % False)
        writer.WriteLine("UwaStandaloneServerExecuteExecuteBox=%s" % True)
        writer.WriteLine("UwaGeneratorMapNumberPerTaskBox=%s" % scriptDialog.GetValue("UwaGeneratorMapNumberPerTaskBox"))
        writer.WriteLine("UwaGeneratorMapNumberBox=%s" % scriptDialog.GetValue("UwaGeneratorMapNumberBox"))
        writer.WriteLine("UwaUhcTypeGeneratorToUseBox=%s" % scriptDialog.GetValue("UwaUhcTypeGeneratorToUseBox"))

    else:
        writer.WriteLine("UwaEnabledExecuteBox=%s" % False)
        writer.WriteLine("UwaStandaloneServerExecuteExecuteBox=%s" % False)

    writer.Close()

    commandsFilename = Path.Combine(ClientUtils.GetDeadlineTempPath(), "commandsfile.txt")
    writer = StreamWriter(commandsFilename, False, Encoding.Unicode)

    for x in range(scriptDialog.GetValue("UwaGeneratorMapNumberBox")):
        for line in scriptDialog.GetItems("CommandsBox"):
            if len(line) > 0:
                writer.WriteLine(line)
            else:
                # This is since we can't have blank lines between commands
                break

    writer.Close()

    # Setup the command line arguments.
    arguments = StringCollection()

    arguments.Add(jobInfoFilename)
    arguments.Add(pluginInfoFilename)
    arguments.Add(commandsFilename)

    results = ClientUtils.ExecuteCommandAndGetOutput(arguments)
    scriptDialog.ShowMessageBox(results, "Submission Results")

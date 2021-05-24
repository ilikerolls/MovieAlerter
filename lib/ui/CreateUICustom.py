from lib.ui.CreateUI import CreateUI
from configparser import ConfigParser
import os
import sys
from lib.ImdbSearcherLib import ImdbSearcherScheduler


class CreateUICustom(CreateUI):
    """
    Edit this class to link Custom actions to your widgets(buttons, etc....)
    """

    def __init__(self, icon_file, app):
        super().__init__(icon_file, app)
        self.config = Config(self)
        self.running = False
        self.imdb_scheduler = None

    def setupUi(self):
        """
        Set up buttons and actions in GUI
        """
        super().setupUi()

        # load previously used settings
        self.config.load_config_file_to_gui()

        # disable the maximize option
        self.disable_maximize()
        # Link up the save button to save configuration
        self.exit_pushButton.clicked.connect(self.exit_button)

        # Link add to list button
        self.blacklist_add_pushButton.clicked.connect(self.add_to_blacklist)
        # Link the enter key to add to blacklist
        self.blacklist_lineEdit.returnPressed.connect(self.add_to_blacklist)

        # Link Del from black list button
        self.blacklist_del_pushButton.clicked.connect(self.remove_from_blacklist)

        # Start button
        self.start_pushButton.clicked.connect(self.start_stop_button)

    def start_stop_button(self):
        """
        Start button pushed. Activates imdb searcher
        """
        if self.running is False:
            self.setWindowTitle('Movie Alerter - Running')
            self.start_pushButton.setText('Stop')
            self.running = True

            self.config.get_cur_app_config()
            self.imdb_scheduler = ImdbSearcherScheduler(self.config.get('MAIN', 'MinRating'),
                                                        self.config.get('MAIN', 'MinVotes'),
                                                        self.config.get_blacklist_as_list(),
                                                        pushbullet_api_key=self.config.get('MAIN', 'PushBulletAPIKey'))
            self.imdb_scheduler.start()
        else:
            self.imdb_scheduler.stop()
            self.setWindowTitle('Movie Alerter - Stopped')
            self.start_pushButton.setText('Start')
            self.running = False

    def add_to_blacklist(self, item=None):
        """
        Adds text from blacklist line edit to blacklist & clears the lineEdit
        :param item: If an item is passed, then add that to the black list instead of blacklist_lineEdit textbox value
        """

        if item:
            self.blacklist_listWidget.addItem(item)
        else:
            if len(self.blacklist_lineEdit.text()) > 0 and not self.blacklist_lineEdit.text().isspace():
                self.blacklist_listWidget.addItem(self.blacklist_lineEdit.text())
                self.blacklist_lineEdit.clear()

    def remove_from_blacklist(self):
        """
        Remove 1 or more selected items from the list
        """
        list_items = self.blacklist_listWidget.selectedItems()

        for item in list_items:
            self.blacklist_listWidget.takeItem(self.blacklist_listWidget.row(item))

    def exit_button(self):
        """
        Save GUI data and exit application when Exit button pushed
        """
        self.config.save_cur_app_config()
        self.quit()


class Config(ConfigParser):
    """
    Configuration class for saving and loading settings
    """

    def __init__(self, pyqt_form, config_file='config.ini'):
        """
        Set instance variables
        :param pyqt_form: Should be CreateUI class or the class of a form
        :param config_file: Configuration filename default '/lib/ui/config.ini'
        """
        super().__init__()
        self.pyqt_form = pyqt_form

        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.config_file_name = os.path.join(base_path, config_file)

    def get_cur_app_config(self):
        """
        Gets all the settings from the GUI and puts them in ConfigParser()
        """
        black_list = ''
        for i in range(self.pyqt_form.blacklist_listWidget.count()):
            black_list += str(self.pyqt_form.blacklist_listWidget.item(i).text()) + ','
        black_list = black_list[:-1]

        self['MAIN'] = {
            'MinRating': self.pyqt_form.doubleSpinBox.value(),
            'MinVotes': self.pyqt_form.spinBox.value(),
            'HourlyCheck': self.pyqt_form.sc_spinBox.value(),
            'PushBulletAPIKey': self.pyqt_form.pb_lineEdit.text(),
            'BoxOfficeUrl': self.pyqt_form.bo_url_lineEdit.text(),
            'blackList': black_list,
        }

    def get_blacklist_as_list(self):
        """
        Return black list as a list instead of a string
        :return: blacklist in list form
        """
        blacklist_list = []
        for item in self.get('MAIN', 'blacklist').split(','):
            blacklist_list.append(item)
        return blacklist_list

    def save_cur_app_config(self):
        """
        Save settings in GUI to the config file
        """
        self.get_cur_app_config()
        with open(self.config_file_name, 'w') as configfile:
            self.write(configfile)

    def load_config_file_to_gui(self):
        """
        Loads configuration file and updates settings GUI app settings based on previous configuration file
        """
        self.read_file(open(self.config_file_name))

        # Add items to black list
        for item in self.get('MAIN', 'blacklist').split(','):
            self.pyqt_form.add_to_blacklist(item)

        # set minimum Rating
        self.pyqt_form.doubleSpinBox.setProperty("value", self.get('MAIN', 'MinRating'))
        # set minimum votes
        self.pyqt_form.spinBox.setProperty("value", self.get('MAIN', 'MinVotes'))
        # set Hourly Check
        self.pyqt_form.sc_spinBox.setProperty("value", self.get('MAIN', 'HourlyCheck'))
        # set Push Bullet API key
        self.pyqt_form.pb_lineEdit.setText(self.get('MAIN', 'PushBulletAPIKey'))
        # set Box Office URL
        self.pyqt_form.bo_url_lineEdit.setText(self.get('MAIN', 'BoxOfficeUrl'))

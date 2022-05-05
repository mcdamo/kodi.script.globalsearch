import pickle
import xbmc
import xbmcaddon
import xbmcvfs
import datetime
from collections import OrderedDict

ADDON = xbmcaddon.Addon()

class AddonData:
    def __init__(self, *args, **kwargs):
        self.path = self._get_addon_storage_path() + kwargs['path']

    def _get_addon_storage_path(self):
        return xbmcvfs.translatePath(ADDON.getAddonInfo('profile')) # addon_data

    def load(self):
        # load from addon storage filesystem
        try:
            return pickle.load(open(self.path, 'rb'))
        except Exception as err:
            xbmc.log("Failed to load file: %s" % err, xbmc.LOGWARNING)
            pass


    def save(self, data):
        try:
            pickle.dump(data, open(self.path, 'wb'))
        except Exception as err:
            xbmc.log("Failed to save file: %s" % err, xbmc.LOGERROR)
            pass

class HistoryData(AddonData):
    def __init__(self, *args, **kwargs):
        super().__init__(args, path='history.p', **kwargs)

    def load(self):
        history = super().load()
        if not history or not isinstance(history, OrderedDict):
            history = OrderedDict()
        return history

    def append(self, searchstring, limit=-1):
        history = self.load()
        if searchstring in history:
            # delete to re-add below
            del history[searchstring]
        while (limit >= 0 and len(history) > limit):
            history.popitem(last=False)
        # new items are appended at the 'end'
        # timestamp is not presently used, but could be sorted on in future.
        history[searchstring] = datetime.datetime.now().timestamp()
        self.save(history)
        return history

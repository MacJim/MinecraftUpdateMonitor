import sqlite3


class DatabaseManager:
# MARK: Database settings
    databaseName = "MinecraftUpdateMonitor"
    databaseFilename = "MinecraftUpdateMonitor.db"

    minecraftDevelopmentVersionsTableName = "MinecraftDevelopmentVersions"
    minecraftReleaseVersionsTableName = "MinecraftReleaseVersions"


# MARK: Singleton stuff
    _sharedInstance = None

    @staticmethod
    def getInstance():
        if (DatabaseManager._sharedInstance is None):
            _sharedInstance = DatabaseManager()

        return _sharedInstance


# MARK: Constructors and destructors
    def __init__(self):
        self.databaseConnection = sqlite3.connect(DatabaseManager.databaseFilename)
        self.databaseConnection.row_factory = sqlite3.Row
        self.databaseConnection.execute("PRAGMA foreign_keys = ON")
        self.databaseCursor = self.databaseConnection.cursor()

    def __del__(self):
        # super.__del__(self)
        if (hasattr(self, "databaseCursor")):
            self.databaseCursor.close()

        if (hasattr(self, "databaseConnection")):
            self.databaseConnection.commit()
            self.databaseConnection.close()


# MARK: Create tables
    def createTables(self):
        createTablesSQLFileContent = open('Documentation/Create tables.sql', 'r').read()
        self.databaseCursor.executescript(createTablesSQLFileContent)
        self.databaseConnection.commit()


# MARK: Minecraft version tables
    def getLatestMinecraftDevelopmentVersionInformation(self):
        self.databaseCursor.execute("SELECT versionID, versionString, datetime(detectedDate, 'unixepoch', 'localtime'), wikiPageURL FROM " + DatabaseManager.minecraftDevelopmentVersionsTableName + " ORDER BY detectedDate DESC LIMIT 1")    # Be sure to add "localtime" or the time returned will be in UTC.
        return self.databaseCursor.fetchone()

    def getAllMinecraftDevelopmentVersionsInformation(self):
        self.databaseCursor.execute("SELECT versionID, versionString, datetime(detectedDate,'unixepoch', 'localtime'), wikiPageURL FROM " + DatabaseManager.minecraftDevelopmentVersionsTableName + " ORDER BY detectedDate DESC")
        return self.databaseCursor.fetchall()

    def addMinecraftDevelopmentVersionInformation(self, versionString, wikiPageURL):
        self.databaseCursor.execute("INSERT INTO " + DatabaseManager.minecraftDevelopmentVersionsTableName + " VALUES(0, ?, strftime('%s', 'now'), ?)", (versionString, wikiPageURL))
        self.databaseConnection.commit()

    def getLatestMinecraftReleaseVersionInformation(self):
        self.databaseCursor.execute(
            "SELECT versionID, versionString, datetime(detectedDate, 'unixepoch', 'localtime'), wikiPageURL FROM " + DatabaseManager.minecraftReleaseVersionsTableName + " ORDER BY detectedDate DESC LIMIT 1")
        return self.databaseCursor.fetchone()

    def getAllMinecraftReleaseVersionsInformation(self):
        self.databaseCursor.execute(
            "SELECT versionID, versionString, datetime(detectedDate, 'unixepoch', 'localtime'), wikiPageURL FROM " + DatabaseManager.minecraftReleaseVersionsTableName + " ORDER BY detectedDate DESC")
        return self.databaseCursor.fetchall()

    def addMinecraftReleaseVersionInformation(self, versionString, wikiPageURL):
        self.databaseCursor.execute("INSERT INTO " + DatabaseManager.minecraftReleaseVersionsTableName + " VALUES(0, ?, strftime('%s', 'now'), ?)", (versionString, wikiPageURL))
        self.databaseConnection.commit()

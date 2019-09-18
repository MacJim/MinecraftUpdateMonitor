--CREATE DATABASE MinecraftUpdateMonitor CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

--USE MinecraftUpdateMonitor;

--ATTACH DATABASE 'MinecraftUpdateMonitor.db' as 'MinecraftUpdateMonitor';


CREATE TABLE MinecraftDevelopmentVersions (
    versionID INTEGER,    -- Make sure to specify the full "INTEGER" type (rather than "INT") to make this column an alias of `rowid`.

    versionString VARCHAR(16),    -- Example: 19w02a, 1.13-pre10

    detectedDate INTEGER,    -- First detected date. UNIX timestamp.

    wikiPageURL TEXT,

    PRIMARY KEY (versionID)
);

CREATE TABLE MinecraftReleaseVersions (
    versionID INTEGER,    -- Make sure to specify the full "INTEGER" type (rather than "INT") to make this column an alias of `rowid`.

    versionString VARCHAR(12),    -- Example: 1.13.2

    detectedDate INTEGER,    -- First detected date. UNIX timestamp.

    wikiPageURL TEXT,

    PRIMARY KEY (versionID)
);
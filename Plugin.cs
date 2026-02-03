using System.Collections.Generic;
using System.IO;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using UnityCommon;
using UnityEngine;

namespace Alba.Spolszczenie;

[BepInPlugin(MyPluginInfo.PLUGIN_GUID, MyPluginInfo.PLUGIN_NAME, MyPluginInfo.PLUGIN_VERSION)]
public class Plugin : BaseUnityPlugin
{
    internal new static ManualLogSource Logger;

    void Awake()
    {
        Logger = base.Logger;
        Logger.LogInfo($"{MyPluginInfo.PLUGIN_GUID} loaded");

        var harmony = new Harmony(MyPluginInfo.PLUGIN_GUID);
        harmony.PatchAll();
    }
}

[HarmonyPatch(typeof(GameTextService), nameof(GameTextService.LoadTextForLanguage))]
static class LoadTextForLanguagePatch
{
    static bool Prefix(TextLanguage language, ref GameTextCollection __result)
    {
        if (language != TextLanguage.French)
            return true;

        var jsonlPath = Path.Combine(Paths.GameRootPath, "alba.pl.jsonl");

        if (!File.Exists(jsonlPath))
        {
            Plugin.Logger.LogWarning($"Polish JSONL not found at: {jsonlPath}");
            return true;
        }

        var collection = ScriptableObject.CreateInstance<GameTextCollection>();
        collection.language = TextLanguage.French;
        collection.rightToLeft = false;
        collection.textContents = new List<GameTextContent>();

        var lines = File.ReadAllLines(jsonlPath);
        foreach (var line in lines)
        {
            if (string.IsNullOrEmpty(line))
                continue;

            var entry = JsonUtility.FromJson<JsonlEntry>(line);
            if (entry != null && !string.IsNullOrEmpty(entry.id))
            {
                collection.textContents.Add(new GameTextContent(entry.id, entry.text));
            }
        }

        Plugin.Logger.LogInfo($"Loaded {collection.textContents.Count} Polish text entries from JSONL");
        __result = collection;
        return false;
    }

    [System.Serializable]
    class JsonlEntry
    {
        public string id;
        public string text;
    }
}

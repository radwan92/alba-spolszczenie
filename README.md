# Alba: A Wildlife Adventure - Spolszczenie

Plugin [BepInEx](https://github.com/BepInEx/BepInEx) dodający polskie tłumaczenie do gry **Alba: A Wildlife Adventure**.

Działa poprzez podmienianie tekstów języka francuskiego na polskie tłumaczenia z pliku `alba.pl.jsonl`. Aby włączyć spolszczenie, w ustawieniach gry należy wybrać **język francuski**.

Projekt korzysta z biblioteki [BepInEx](https://github.com/BepInEx/BepInEx) do wstrzykiwania kodu oraz [HarmonyX](https://github.com/BepInEx/HarmonyX) do patchowania metod gry w runtime. Wymagane pliki BepInEx znajdują się w katalogu `Injection\`.

## Budowanie

### Konfiguracja ścieżki do gry

Projekt wymaga dostępu do katalogu instalacji gry Alba. Domyślna ścieżka to:

```
C:\Program Files\Epic Games\AlbaAWildlifeAdventusiuFk
```

Jeśli gra jest zainstalowana w innym miejscu, ścieżkę można zmienić na kilka sposobów:

**Opcja 1 - `Directory.Build.props` (zalecane)**

Utwórz plik `Directory.Build.props` w katalogu projektu:

```xml
<Project>
  <PropertyGroup>
    <AlbaDir>D:\Gry\Alba</AlbaDir>
  </PropertyGroup>
</Project>
```

Plik ten jest ignorowany przez git i nie wpłynie na konfigurację innych osób.

**Opcja 2 - parametr wiersza poleceń**

```bash
dotnet build -p:AlbaDir="D:\Gry\Alba"
```

### Kompilacja

```bash
dotnet build
```

### Kopiowanie plików do katalogu gry

Domyślnie kompilacja **nie kopiuje** plików do katalogu gry. Aby włączyć automatyczne kopiowanie, użyj parametru `CopyToGame`:

```bash
dotnet build -p:CopyToGame=true
```

Lub dodaj go na stałe w `Directory.Build.props`:

```xml
<CopyToGame>true</CopyToGame>
```

Po włączeniu do katalogu gry zostaną skopiowane:

- pliki BepInEx z katalogu `Injection\` (loader, doorstop)
- plugin `Alba.Spolszczenie.dll` do `<AlbaDir>\BepInEx\plugins`
- plik tłumaczenia `alba.pl.jsonl` do katalogu głównego gry

## Instalacja ręczna

1. Skopiuj zawartość katalogu `Injection\` do katalogu głównego gry (BepInEx, `doorstop_config.ini`, `winhttp.dll`)
2. Skopiuj `Alba.Spolszczenie.dll` do `<katalog gry>\BepInEx\plugins`
3. Skopiuj `alba.pl.jsonl` do katalogu głównego gry
4. W ustawieniach gry zmień język na **francuski**

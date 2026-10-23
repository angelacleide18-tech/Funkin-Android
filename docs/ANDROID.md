# Android playtest build

The `preview/public-playtest` branch already includes native Android support,
landscape display, touch controls, haptics and Android mod-folder integration.
The separate **Build Android APK** workflow builds this existing port on a
GitHub-hosted runner, without the upstream team's self-hosted runners, GitHub
App credentials, private asset aliases or store signing secrets.

## Download a test APK

1. Open **Actions > Build Android APK** after the workflow is added to the repository.
2. Open a successful run for `preview/public-playtest` and download the
   `Funkin-Android-arm64-debug` artifact.
3. Extract the ZIP and install the APK on a physical ARM64 Android device.
   Android may ask you to allow installation from the app opening the APK.

The workflow runs on relevant pushes and pull requests targeting
`preview/public-playtest`. Manual **Run workflow** availability requires the
workflow to also exist on the repository's default branch.

This is a debug-signed playtest APK, not a Play Store release. It targets
ARM64 devices running Android 9 (API 28) or newer, as required by the pinned
Lime version. It does not support ARMv7-only phones or x86 emulators. Android
will not install it over an app with the same package name and a different
signature. Back up saves before removing an existing installation. GitHub
runner debug keys may also differ between runs.

## Build locally

Follow the Haxe dependency installation in [COMPILING.md](COMPILING.md), using
Haxe **4.3.7** and the dependencies pinned in `hmm.json`. Initialize both public
asset submodules at their recorded commits:

```bash
git submodule update --init --depth 1 assets art
```

Install JDK **17**, Android SDK platform **36**, build tools **36.0.0** and NDK
**27.2.12479018**. Set `JAVA_HOME` to the JDK, `ANDROID_SDK` to the SDK directory
and `ANDROID_NDK_ROOT` to that NDK installation. For example, on Linux with the
SDK already installed and `sdkmanager` on `PATH`:

```bash
sdkmanager "platform-tools" "platforms;android-36" "build-tools;36.0.0" "ndk;27.2.12479018"
export ANDROID_SDK="$ANDROID_HOME"
export ANDROID_NDK_ROOT="$ANDROID_HOME/ndk/27.2.12479018"
haxelib run lime rebuild android -debug -arm64
haxelib run lime build android -debug -arm64 -DEXCLUDE_ARMV7 -DNO_REDIRECT_ASSETS_FOLDER
```

When using Lime from Git, build its native host library before the Android
commands above (`haxelib run lime rebuild cpp -64` on Linux). The workflow
installs the Linux development libraries needed for this step. Other host
platforms need their native build toolchain as described in the compiling guide.

The APK is written under
`export/debug/android/bin/app/build/outputs/apk/debug/`. Install with
`adb install -r <path-to-apk>` or copy it to the phone. No `.env` or production
signing key is required. The debug build does not enable production ads,
in-app purchases or release-only ASTC texture compression by default; its
memory use and performance are not representative of an optimized release.

## Validation before distribution

A successful workflow confirms compilation and packaging only. On a real
device, verify startup, landscape layout, menu navigation, simultaneous note
touches, held notes, pause/back navigation, audio, video cutscenes, background
and resume, and save persistence after restarting. Test memory use during a
full song before distributing to other players.

The asset submodules retain their own licenses. If a recorded asset commit
cannot be downloaded, restore access to that exact revision; do not replace it
with the latest assets from a different game version.

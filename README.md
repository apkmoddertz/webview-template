# Web2App Android WebView Template

This repository is a real Android WebView wrapper template for a Web-to-App Builder. It packages a website inside an Android APK; it does **not** convert a website into native Android code.

## Default project

- App name: `Web2App`
- Website: `https://example.com`
- Package/application ID: `com.web.app`
- JDK: 17
- Gradle: 8.7 wrapper
- Android Gradle Plugin: 8.6.1
- compileSdk/targetSdk: 35
- minSdk: 21

## How it works

`app/src/main/assets/config.json` contains `appName`, `appUrl`, and `packageName`. `MainActivity` reads `appUrl` at runtime and loads it in a WebView. If the file is missing or invalid, it safely falls back to `https://example.com`.

The WebView enables JavaScript and DOM storage, uses a `WebViewClient` for in-app navigation, supports the Android back button, and uses normal HTTPS certificate validation. Only the INTERNET permission is requested.

## GitHub Actions build

1. Upload the contents of this repository to GitHub.
2. Open **Actions → Build APK → Run workflow**. The workflow automatically accepts Android SDK licenses and installs `platform-tools`, `platforms;android-35`, and `build-tools;35.0.0` before compiling.
3. Enter:
   - **App name**: display name for the APK/app
   - **Website URL**: an `http://` or `https://` URL
   - **Package name**: for example `com.test.app`
   - **Logo URL**: optional direct PNG URL; leave empty to use the built-in default icon
4. Start the workflow. The job validates inputs, updates `config.json`, application ID, and app name, optionally downloads and scales the logo into launcher icons, builds a release APK, uploads it as the `android-apk` artifact, and creates a GitHub Release.
5. Download the APK from the workflow run's **Artifacts** section or the created GitHub Release.

The workflow uses `${{ secrets.GITHUB_TOKEN }}` through the GitHub Actions release action. No personal access token is placed in the Android application and no token is hard-coded.

## Temporary signing key limitation

For this prototype, each workflow run creates a temporary signing keystore. Every build therefore has a different signing key and normally cannot be installed as an update over a previous build. A production builder should use a protected, persistent release keystore stored in GitHub encrypted secrets.

## WebView limitations

WebView behavior depends on the target website and Android System WebView. Some websites may block embedded browsers, require features not available in WebView, or need additional handling for downloads, file uploads, notifications, deep links, or authentication. This template intentionally avoids unsafe JavaScript interfaces, broad file access, cleartext traffic, and SSL-error bypasses.

## AndroidIDE

Copy or extract the repository so the project root is the folder containing `settings.gradle`, `build.gradle`, `gradlew`, and the `app` folder. In AndroidIDE, choose **Open existing project** and select that root. The Android source is already at `app/src/main`, including `AndroidManifest.xml`, `assets`, `java/com/web/app`, and `res`.

If AndroidIDE asks for a Gradle JDK, select JDK 17. Allow it to sync and install Android SDK Platform 35 and Build Tools 35.x if prompted. Then use **Build → Assemble Debug** or run `./gradlew assembleDebug` from the project terminal. The debug APK will be under `app/build/outputs/apk/debug/`.

To customize a local build, edit `app/src/main/assets/config.json` and `app/src/main/res/values/strings.xml`. Keep the URL HTTP/HTTPS and keep the Java package directory unless you also refactor the Java package declaration.

## Future architecture

The intended system is: user → Web-to-App Builder → Cloudflare Worker → GitHub Actions → customized repository build → APK download. The Cloudflare Worker should validate and securely dispatch the workflow; it should never expose GitHub credentials to the APK.

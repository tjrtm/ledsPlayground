# Build apk 
npm install -g cordova

cordova build android

# requirements
* Java 11
* Gradle


## 1. Install Gradle
The error message indicates that Gradle, a build automation tool required for Android development, is not installed or not found in your system path. Here’s how you can install it:

- **Download Gradle**: Visit the [Gradle Releases Page](https://gradle.org/releases/) and download the latest Gradle distribution.
- **Extract the Distribution**: Unzip the downloaded archive into a directory on your computer, for example, `C:\Gradle`.
- **Set Environment Variables**:
  - Right-click on 'My Computer' or 'This PC' and select 'Properties'.
  - Click on 'Advanced system settings' and then 'Environment Variables'.
  - Under 'System Variables', click 'New' to create a new variable:
    - Variable name: `GRADLE_HOME`
    - Variable value: `C:\Gradle\gradle-x.x` (replace `x.x` with the version you downloaded)
  - Find the `Path` variable in 'System Variables' and click 'Edit'.
  - Add a new entry: `%GRADLE_HOME%\bin`
  - Click 'OK' to close all dialogs.
- **Verify Installation**: Open a new command prompt and type `gradle -v` to check if Gradle is installed correctly. It should display the Gradle version.

## 2. Set Android SDK Environment Variables
The message about `ANDROID_HOME` being undefined and `ANDROID_SDK_ROOT` being deprecated suggests that your environment variables for the Android SDK are not correctly set. Here’s how to set them up:

- **Set `ANDROID_SDK_ROOT`** (also can add `ANDROID_HOME` but it is deprecated):
  - Under 'System Variables', click 'New' to create a new variable:
    - Variable name: `ANDROID_SDK_ROOT`
    - Variable value: `C:\Users\{USER}\AppData\Local\Android\sdk` (based on your provided SDK location)
  - Add the SDK's `tools` and `platform-tools` directories to your system `Path` variable:
    - `%ANDROID_SDK_ROOT%\tools`
    - `%ANDROID_SDK_ROOT%\platform-tools`

## 3. Check Java JDK Installation
Make sure you have Java JDK installed:

- **Verify Java Installation**: Open a command prompt and type `java -version` and `javac -version`. Both should return the version of Java installed.
- **Set JAVA_HOME**:
  - If not set, under 'System Variables', click 'New' to create a new variable:
    - Variable name: `JAVA_HOME`
    - Variable value: path to your JDK, e.g., `C:\Program Files\Java\jdk-xx.xx.x_xx` ( use jdk-11.x.x)
  - Add `%JAVA_HOME%\bin` to your system `Path` variable.

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "jp.mastiff.okanesagashi"
    compileSdk = 35

    defaultConfig {
        applicationId = "jp.mastiff.okanesagashi"
        minSdk = 26
        targetSdk = 35
        versionCode = 10
        versionName = "1.2.2"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            // 個人用：デバッグ鍵で署名（ストアには出さないため）
            signingConfig = signingConfigs.getByName("debug")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.activity:activity-ktx:1.9.3")
    implementation("androidx.webkit:webkit:1.12.1")
}

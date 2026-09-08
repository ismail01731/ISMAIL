plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.compose)
}

android {
    namespace = "com.ismail.ai"
    compileSdk {
        version = release(37)
    }

    defaultConfig {
        applicationId = "com.ismail.ai"
        minSdk = 24
        targetSdk = 37
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            optimization {
                enable = false
            }
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    buildFeatures {
        compose = true
    }
}

dependencies {
    implementation("com.microsoft.onnxruntime:onnxruntime-android:1.29.0")
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.activity.compose)
    implementation(libs.androidx.compose.material3)
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.ui.graphics)
    implementation(libs.androidx.compose.ui.tooling.preview)
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    testImplementation(libs.junit)
    androidTestImplementation(platform(libs.androidx.compose.bom))
    androidTestImplementation(libs.androidx.compose.ui.test.junit4)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(libs.androidx.junit)
    debugImplementation(libs.androidx.compose.ui.test.manifest)
    debugImplementation(libs.androidx.compose.ui.tooling)
    implementation("androidx.webkit:webkit:1.14.0")
}
tasks.register("syncFrontendAssets") {
    val frontendDir = rootProject.file("frontend")
    val assetsDir = project.file("src/main/assets")
    doLast {
        val filesToSync = listOf(
            "index.html",
            "manifest.json",
            "script.js",
            "style.css",
            "sw.js"
        )
        assetsDir.mkdirs()
        filesToSync.forEach { fileName ->
            val source = frontendDir.resolve(fileName)
            val target = assetsDir.resolve(fileName)
            if (!source.exists()) {
                throw GradleException("Frontend asset not found: ${source.absolutePath}")
            }
            source.copyTo(target, overwrite = true)
        }
    }
}
tasks.named("preBuild") {
    dependsOn("syncFrontendAssets")
}

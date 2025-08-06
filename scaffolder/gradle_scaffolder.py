# scaffolder/gradle_scaffolder.py

import os
from pathlib import Path

BUILD_GRADLE = """
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.1.0'
}

group = '{PACKAGE_GROUP}'
version = '1.0.0'
sourceCompatibility = '17'

repositories {
    mavenCentral()
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
}
"""

SETTINGS_GRADLE = "rootProject.name = '{PROJECT_NAME}'\n"


def scaffold_gradle_project(output_dir: Path, package: str):
    project_name = output_dir.name
    package_path = package.replace(".", "/")
    java_src_path = output_dir / "src" / "main" / "java" / package_path

    # Create all folders
    java_src_path.mkdir(parents=True, exist_ok=True)
    (output_dir / "src" / "main" / "resources").mkdir(parents=True, exist_ok=True)

    # Create build.gradle
    build_file = output_dir / "build.gradle"
    build_file.write_text(BUILD_GRADLE.replace("{PACKAGE_GROUP}", package))

    # Create settings.gradle
    settings_file = output_dir / "settings.gradle"
    settings_file.write_text(SETTINGS_GRADLE.replace("{PROJECT_NAME}", project_name))


def save_java_file(java_code: str, class_name: str, output_dir: Path, package: str):
    package_path = package.replace(".", "/")
    java_file_path = output_dir / "src" / "main" / "java" / package_path / f"{class_name}.java"
    java_file_path.write_text(java_code)

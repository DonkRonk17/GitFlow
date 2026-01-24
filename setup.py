#!/usr/bin/env python3
"""GitFlow - Smart Git Workflow Assistant

A zero-dependency CLI tool for conventional commits, branch management,
repository statistics, and changelog generation.

Part of the Team Brain ecosystem.
"""
from setuptools import setup
from pathlib import Path

readme = Path(__file__).parent / "README.md"
long_description = readme.read_text(encoding='utf-8') if readme.exists() else ""

setup(
    name="gitflow",
    version="1.0.0",
    description="Smart git workflow assistant - conventional commits, branch management, stats, changelog generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Randell Logan Smith",
    author_email="logan@metaphysicsandcomputing.com",
    url="https://github.com/DonkRonk17/GitFlow",
    py_modules=["gitflow"],
    install_requires=[],
    entry_points={"console_scripts": ["gitflow=gitflow:main"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.6",
    keywords="git workflow conventional-commits changelog branch-management developer-tools cli zero-dependencies",
    project_urls={
        "Bug Reports": "https://github.com/DonkRonk17/GitFlow/issues",
        "Source": "https://github.com/DonkRonk17/GitFlow",
        "Company": "https://metaphysicsandcomputing.com",
    },
)

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dp-student-analytics",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Differential Privacy Student Analytics System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dp-student-analytics",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/dp-student-analytics/issues",
        "Documentation": "https://github.com/yourusername/dp-student-analytics/blob/main/README.md",
        "Source Code": "https://github.com/yourusername/dp-student-analytics",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.28.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
        "plotly>=5.0.0",
        "scipy>=1.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
            "jupyter>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "dp-analytics=streamlit.cli:main",
        ],
    },
    keywords=[
        "differential-privacy",
        "privacy-preserving",
        "student-analytics",
        "data-privacy",
        "machine-learning",
        "educational-data",
    ],
    zip_safe=False,
)

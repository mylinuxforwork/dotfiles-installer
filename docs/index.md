---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "The ML4W Dotfiles Installer"
  image:
    src: /com.ml4w.dotfilesinstaller.svg
    alt: Linux logo
    style: "width: 200px; height: auto;"  
  tagline: Install dotfiles easy, fast and secure. 
  actions:
    - theme: brand
      text: Get Started
      link: /geting-started
    - theme: alt
      text: Install
      link: /getting-started/install
    - theme: alt
      text: GitHub ↗
      link: https://github.com/mylinuxforwork/dotfiles-installer

features:
  - title: Installation Wizzard
    details: Easy to use and guided installation w of multiple dotfiles in parallel
  - title: Backup and Protection
    details: Backup of existing configuration and protection of your personal customization
  - title: Publish your own dotfiles
    details: The integrated development workflow supports you to You can create and publish your personal dotfiles for everyone
---

### 1. Installation

Install the Dotfiles Installer by running the following command in your terminal:

```sh
bash -c "$(curl -s https://raw.githubusercontent.com/mylinuxforwork/dotfiles-installer/master/setup.sh)"

```
### 2. Load the .dotinst

Copy the path to the .dotinst file into the Load Configuration entry field, click on Load and follow the installation wizzard.

<img
  src="/mainscreen.jpg"
  alt="preview"
  style="max-width: 900px; width: 100%; border-radius: 12px; margin: 2rem auto; display: block;"
/>

<style>
:root {
  --vp-home-hero-name-color: transparent;
  --vp-home-hero-name-background: -webkit-linear-gradient(120deg, var(--vp-c-purple-3), var(--vp-c-brand-3));
  --vp-home-hero-image-filter: blur(44px);

  --overlay-gradient: color-mix(in srgb, var(--vp-c-brand-1), transparent 40%);
}

.dark {
  --overlay-gradient: color-mix(in srgb, var(--vp-c-brand-1), transparent 75%);
}

.home-page {
  background:
    linear-gradient(200deg, transparent 25%, var(--overlay-gradient) 55%, transparent 85%),
    radial-gradient(ellipse at 80% 180%, var(--overlay-gradient), transparent 60%),
    var(--vp-c-bg);
  background-repeat: no-repeat;
  background-size: cover;

  .VPFeature a {
    font-weight: bold;
    color: var(--vp-c-brand-2);
  }

  .VPFooter {
    background-color: transparent !important;
    border: none;
  }

  .VPNavBar {
    background-color: transparent !important;
    -webkit-backdrop-filter: blur(16px);
    backdrop-filter: blur(16px);

    div.divider {
      display: none;
    }
  }
}

@media (min-width: 640px) {
  :root {
    --vp-home-hero-image-filter: blur(56px);
  }
}

@media (min-width: 960px) {
  :root {
    --vp-home-hero-image-filter: blur(68px);
  }
}
</style>
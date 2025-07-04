// .vitepress/config.ts
export default {
  title: 'ML4W Dotfiles Installer Wiki',
  description: 'Easy installer app for dotfiles configurations',
  base: "/dotfiles-installer/",
  lastUpdated: true,
  cleanUrls: true,

  head: [
    ["link", { rel: "icon", href: "com.ml4w.dotfilesinstaller.svg" }],
  ],

  themeConfig: {
    siteTitle: "ML4W Dotfiles Installer",
    logo: "/com.ml4w.dotfilesinstaller.svg",
    outline: "deep",
    docsDir: "/docs",
    editLink: {
      pattern: "https://github.com/mylinuxforwork/dotfiles-installer/tree/master/docs/:path",
      text: "Edit this page on GitHub",
    },
    nav: [
      { text: "Home", link: "/" },
      { text: "About", link: "/getting-started/overview" },
      {
        text: "Examples",
        link: "/examples",
        activeMatch: "/examples/",
      },
     {
        text: "0.8.4",
        items: [
          {
            text: 'Changelog',
            link: 'https://github.com/mylinuxforwork/dotfiles-installer/blob/master/CHANGELOG.md'
          },
        ],
      },
      {
        text: "More",
        items: [
          {
            text: 'ML4W Dotfiles for Hyprland',
            link: 'https://mylinuxforwork.github.io/dotfiles/'
          },
          {
            text: 'ML4W Hyprland Starter',
            link: 'https://github.com/mylinuxforwork/hyprland-starter'
          },
          {
            text: 'Wallpapers',
            link: 'https://github.com/mylinuxforwork/wallpaper'
          },
          {
           text: 'Contributing to wiki →',
           link: '/development/wiki'
          },
          {
           text: 'Troubleshooting →',
           link: '/help/troubleshooting'
          },
        ],
      },
    ],

    sidebar: {
    // future feature may be needed: sep sidebar for dots-installer section or any other
    // basicallyy when user visits /dots-installer/ page it will only show dots-installer menu items
    // just like how vitepress docs sep "refrence" section https://vitepress.dev/

     // '/dots-installer/': [
     //   {
     //    text: "Dots Installer",
     //    items: [
     //       { text: "Overview", link: "/dots-installer/overview" },
     //       { text: "Installation", link: "/dots-installer/installation" },
     //       { text: "Dots Installation", link: "/dots-installer/dots-installation" },
     //       { text: "Dots File", link: "/dots-installer/dots-file" },
     //     ],
     //   },
     // ],

    // default sidebar '/' that shows for all pages except those with specific sidebar rules above...

      '/': [
        {
          text: "Getting Started",
          // collapsed: false,
          items: [
            { text: "Overview", link: "/getting-started/overview" },
            { text: "Install", link: "/getting-started/install" },
            { text: "Dependencies", link: "/getting-started/dependencies" },
            { text: "Install Options", link: "/getting-started/options" },
            { text: "Install in VM (KVM)", link: "/getting-started/vm-install" },
            { text: "Update", link: "/getting-started/update" },
          ],
        },
        {
          text: "Configuration",
          collapsed: true,
          items: [
            { text: "Preserve Config & Customize", link: "/configuration/preserve-config" },
            { text: "Auto Setup & Update", link: "/configuration/auto-setup" },
            { text: "Use on Other Distros", link: "/configuration/distros" },
            { text: "Monitor Setup", link: "/configuration/monitor-setup" },
            { text: "Hyprland + NVIDIA", link: "/configuration/hypr-nvidia" },
            { text: "Switch SDL (X11/Wayland)", link: "/configuration/xwayland" },
          ],
        },
        {
          text: "Usage",
          collapsed: true,
          items: [
            { text: "Launch Hyprland", link: "/usage/launch" },
            { text: "Keybindings", link: "/usage/keybindings" },
            { text: "Screenshots", link: "/usage/screenshots" },
            { text: "Game Mode", link: "/usage/game-mode" },
            { text: "Wallpapers", link: "/usage/wallpapers" },
            { text: "Power & Screenlock", link: "/usage/power-lock" },
          ],
        },
        {
          text: "Customization",
          collapsed: true,
          items: [
            { text: "Dotfiles Customization", link: "/customization/dotfiles" },
            { text: "Config Variants", link: "/customization/variants" },
            { text: "Customize Waybar", link: "/customization/waybar" },
            { text: "Shell (Zsh & Bash)", link: "/customization/shell" },
            { text: "Default Terminal", link: "/customization/terminal" },
            { text: "Default Browser", link: "/customization/browser" },
          ],
        },
        {
          text: "ML4W Apps",
          collapsed: true,
          items: [
            { text: "Welcome App", link: "/ml4w-apps/welcome" },
            { text: "Sidebar App", link: "/ml4w-apps/sidebar" },
            { text: "Dotfiles Settings", link: "/ml4w-apps/dotfiles-app" },
            { text: "Hyprland Settings", link: "/ml4w-apps/hyprland-app" },
          ],
        },
        {
          text: "Help",
          // collapsed: false,
          items: [
            { text: "Troubleshooting", link: "/help/troubleshooting" },
          ],
        },
        {
          text: "Development",
          collapsed: true,
          items: [
            { text: "Contributing to wiki", link: "development/wiki" },
          ]
        },
      ],
    },

    socialLinks: [
      { icon: "discord", link: "https://discord.gg/c4fJK7Za3g" },
      { icon: "github", link: "https://github.com/mylinuxforwork" },
      { 
        icon: {
        svg: '<img src="https://raw.githubusercontent.com/mylinuxforwork/dotfiles-installer/refs/heads/master/data/icons/hicolor/scalable/apps/com.ml4w.dotfilesinstaller.svg" width="24" height="24" alt="dots installer" />'
      }, 
        link: "https://github.com/mylinuxforwork/dotfiles-installer" 
      },
    ],

    footer: {
      message: "Released under the GPL License",
      copyright: `<a href="https://ml4w.com" target="_blank">
        <img src="/dotfiles/ml4w.png" alt="ML4W" />
        Copyright © 2025 Stephan Raabe
      </a>`,
    },

    search: {
      provider: "local",
    },

    returnToTopLabel: 'Go to Top',
    sidebarMenuLabel: 'Menu',
  },
};

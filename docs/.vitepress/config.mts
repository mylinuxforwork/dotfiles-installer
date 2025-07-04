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
          ],
        },
        {
          text: "Install Dotfiles",
          // collapsed: false,
          items: [
            { text: "Load a .dotinst File", link: "/install/load-dotinst" },
            { text: "Backup your configuration", link: "/install/backup" },
            { text: "Define Settings", link: "/install/settings" },
            { text: "Run the Installation", link: "/install/installation" },
          ],
        },
        {
          text: "For Developers",
          // collapsed: false,
          items: [
            { text: "Create a project", link: "/dev/create-project" },
            { text: "Prepare a GitHub repository", link: "/dev/prepare-git-repository" },
            { text: "Sync files", link: "/dev/sync-files" },
            { text: "Publish your Dotfiles", link: "/dev/publish-dotfiles" },
            { text: "Example .dotinst files", link: "/dev/examples" },
          ],
        },
      ],
    },

    socialLinks: [
      { icon: "github", link: "https://github.com/mylinuxforwork" },
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

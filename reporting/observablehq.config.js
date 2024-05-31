// See https://observablehq.com/framework/config for documentation.
export default {
  // The project’s title; used in the sidebar and webpage titles.
  title: "Cumulus Data Metrics",

  // The pages and sections in the sidebar. If you don’t specify this option,
  // all pages will be listed in alphabetical order. Listing pages explicitly
  // lets you organize them into sections and have unlisted pages.
  pages: [
      {name: "Population", pages: [
        {name: "Patient Overview", path: "/index"},
      ]},
      {name: "Resources", pages: [
        {name: "Resource Overview", path: "/resources"},
        {name: "Quality Checks", path: "/quality"},
        {name: "Terminology Use", path: "/terminology"},
        {name: "US Core Elements", path: "/us-core"},
      ]},
      {name: "Metadata", pages: [
        {name: "Metric Tables", path: "/metadata"},
      ]}
  ],

  // Content to add to the head of the page, e.g. for a favicon:
  head: '<link rel="icon" href="logo.png" type="image/png">',

  // The path to the source root.
  root: "src",

  // Some additional configuration options and their defaults:
  // theme: "default", // try "light", "dark", "slate", etc.
  // header: "", // what to show in the header (HTML)
  // footer: "Built with Observable.", // what to show in the footer (HTML)
  // sidebar: true, // whether to show the sidebar
  // toc: true, // whether to show the table of contents
  // pager: true, // whether to show previous & next links in the footer
  // output: "dist", // path to the output root for build
  // search: true, // activate search
  // linkify: true, // convert URLs in Markdown to links
  // typographer: false, // smart quotes and other typographic improvements
  // cleanUrls: true, // drop .html from URLs
};

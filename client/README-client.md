# AI Rules: client

The client part is where all the code related to the front-end is stored. It is a Next.js application, which is a React framework. The client is a web application that can be run in a browser. It is the part of the project that the user will interact with.

## 1. Run the client in localhost

To run the client in localhost, you need to first open a terminal, go to the client directory and run the following command:

<code> npm install </code>

This will install all the dependencies of the client. Then you can run the client with the following command:

`npm run dev`

This should give you the following message in the terminal :

<pre>
> client@0.1.0 dev
> next dev

▲ Next.js 14.0.3

- Local: http://localhost:3000

✓ Ready in 3s
</pre>

You can then open a browser and go to the following address: http://localhost:3000 to see the client running.

## 2. Architecture of the repository

### A. app

This directory contains the pages of the client. Each page is a React component. (Here there is only one page)

### B. components

This directory contains all the React components used in the client. They are divided into two subdirectories: ui and the rest. The ui directory contains the components that are used to build the user interface. The rest of the directory contains the other components.

### C. public

This directory contains all the static files (such as pictures) used in the client.

### D. config files

These files are essential for the client to work :

<code> package-json </code> : contains the dependencies of the client that need to be installed with the command <code> npm install </code>
<code> tailwing.config</code> : contains the general style of the client and the animations

## 3. Roadmap

The nexts steps will be to :

- Keep stored the previous conversations of the user and make them accessible in the sidebar
- Add streaming for displaying the messages in real time (rather than a pop-up)

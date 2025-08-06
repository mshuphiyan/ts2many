// === ts_parser/ts_morph_bridge.js ===
const { Project } = require("ts-morph");
const fs = require("fs");

// Parse CLI arguments
const args = process.argv.slice(2);
let inputPath = null;
let outputPath = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--input") {
    inputPath = args[i + 1];
    i++;
  } else if (args[i] === "--output") {
    outputPath = args[i + 1];
    i++;
  }
}

if (!inputPath) {
  console.error("❌ Usage: node ts_morph_bridge.js --input <file.ts> [--output <output.json>]");
  process.exit(1);
}

// Process file
const project = new Project();
const sourceFile = project.addSourceFileAtPath(inputPath);

const classes = sourceFile.getClasses().map(cls => {
  return {
    name: cls.getName(),
    decorators: cls.getDecorators().map(d => d.getFullText().trim()),
    extends: cls.getExtends()?.getText() || null,
    implements: cls.getImplements().map(i => i.getText()),
    properties: cls.getProperties().map(p => ({
      name: p.getName(),
      type: p.getType().getText(),
      isReadonly: p.isReadonly(),
      isStatic: p.isStatic(),
      access: p.getScope() || "public"
    })),
    constructorParams: (cls.getConstructors()[0]?.getParameters() || []).map(p => ({
      name: p.getName(),
      type: p.getType().getText(),
      decorators: p.getDecorators().map(d => d.getFullText().trim())
    })),
    methods: cls.getMethods().map(m => ({
      name: m.getName(),
      returnType: m.getReturnType().getText(),
      parameters: m.getParameters().map(p => ({
        name: p.getName(),
        type: p.getType().getText()
      }))
    }))
  };
});

const json = JSON.stringify(classes, null, 2);

if (outputPath) {
  fs.writeFileSync(outputPath, json);
  console.log(`✅ AST written to ${outputPath}`);
} else {
  console.log(json);
}

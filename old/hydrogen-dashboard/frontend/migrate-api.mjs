// migrate-api-direct.mjs
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// Get the current directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Directory to search
const directory = path.join(__dirname, "src");

// Create the services directory if it doesn't exist
const servicesDir = path.join(directory, "services");
if (!fs.existsSync(servicesDir)) {
  fs.mkdirSync(servicesDir, { recursive: true });
  console.log(`Created directory: ${servicesDir}`);
}

// Create the new API service file
const apiServiceContent = `// src/services/api.js
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000/api";

export const hydrogenService = {
  async calculateTotalDemand(data) {
    try {
      const response = await axios.post(\`\${API_BASE_URL}/hydrogen-demand/total\`, data);
      return response.data;
    } catch (error) {
      console.error("Error calculating total hydrogen demand:", error);
      throw error;
    }
  },
  
  async calculateAircraftDemand(data) {
    try {
      const response = await axios.post(\`\${API_BASE_URL}/hydrogen-demand/aircraft\`, data);
      return response.data;
    } catch (error) {
      console.error("Error calculating aircraft hydrogen demand:", error);
      throw error;
    }
  },
  
  async calculateGseDemand(data) {
    try {
      const response = await axios.post(\`\${API_BASE_URL}/hydrogen-demand/gse\`, data);
      return response.data;
    } catch (error) {
      console.error("Error calculating GSE hydrogen demand:", error);
      throw error;
    }
  }
};

export const storageService = {
  async calculateStorageCost(data) {
    try {
      const response = await axios.post(\`\${API_BASE_URL}/storage/calculate\`, data);
      return response.data;
    } catch (error) {
      console.error("Error calculating storage cost:", error);
      throw error;
    }
  }
};

export const economicService = {
  async calculateEconomicImpact(data) {
    try {
      const response = await axios.post(\`\${API_BASE_URL}/economic/impact\`, data);
      return response.data;
    } catch (error) {
      console.error("Error calculating economic impact:", error);
      throw error;
    }
  }
};

export default {
  hydrogenService,
  storageService,
  economicService
};`;

fs.writeFileSync(path.join(servicesDir, "api.js"), apiServiceContent, "utf8");
console.log(`Created file: ${path.join(servicesDir, "api.js")}`);

// Function to recursively process files
function processDirectory(dir) {
  const files = fs.readdirSync(dir);

  files.forEach((file) => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      processDirectory(filePath);
    } else if (
      (file.endsWith(".vue") || file.endsWith(".js")) &&
      file !== "api.js" &&
      !filePath.includes("/services/")
    ) {
      let content = fs.readFileSync(filePath, "utf8");
      let modified = false;

      // Replace import statements
      const importRegex = /import\s+{([^}]*)}\s+from\s+['"]\.\.?\/api\.js['"]/g;
      let match;

      while ((match = importRegex.exec(content)) !== null) {
        const imports = match[1];
        const newImports = [];

        if (imports.includes("submitHydrogenDemand"))
          newImports.push("hydrogenService");
        if (imports.includes("submitHydrogenDemandAC"))
          newImports.push("hydrogenService");
        if (imports.includes("submitHydrogenDemandGSE"))
          newImports.push("hydrogenService");
        if (imports.includes("submitStorage"))
          newImports.push("storageService");
        if (imports.includes("submitFinancialAnalysis"))
          newImports.push("economicService");

        // Remove duplicates
        const uniqueImports = [...new Set(newImports)];

        // Create new import statement
        const relativePath =
          filePath.includes("/components/") || filePath.includes("/views/")
            ? "../"
            : "./";
        const newImportStatement = `import { ${uniqueImports.join(
          ", "
        )} } from "${relativePath}services/api.js"`;

        // Replace the entire import statement
        content = content.replace(match[0], newImportStatement);
        modified = true;
      }

      // Replace function calls
      if (content.includes("submitHydrogenDemand(")) {
        content = content.replace(
          /submitHydrogenDemand\(/g,
          "hydrogenService.calculateTotalDemand("
        );
        modified = true;
      }

      if (content.includes("submitHydrogenDemandAC(")) {
        content = content.replace(
          /submitHydrogenDemandAC\(/g,
          "hydrogenService.calculateAircraftDemand("
        );
        modified = true;
      }

      if (content.includes("submitHydrogenDemandGSE(")) {
        content = content.replace(
          /submitHydrogenDemandGSE\(/g,
          "hydrogenService.calculateGseDemand("
        );
        modified = true;
      }

      if (content.includes("submitStorage(")) {
        content = content.replace(
          /submitStorage\(/g,
          "storageService.calculateStorageCost("
        );
        modified = true;
      }

      if (content.includes("submitFinancialAnalysis(")) {
        content = content.replace(
          /submitFinancialAnalysis\(/g,
          "economicService.calculateEconomicImpact("
        );
        modified = true;
      }

      if (modified) {
        console.log(`Updated: ${filePath}`);
        fs.writeFileSync(filePath, content, "utf8");
      }
    }
  });
}

// Start processing
processDirectory(directory);

// Delete the old api.js file if it exists
const oldApiFile = path.join(directory, "api.js");
if (fs.existsSync(oldApiFile)) {
  fs.unlinkSync(oldApiFile);
  console.log(`Deleted old API file: ${oldApiFile}`);
}

console.log("Direct migration complete!");

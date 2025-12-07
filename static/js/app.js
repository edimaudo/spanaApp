
// DOM Elements
const form = document.getElementById('brainstormForm');
const generateBtn = document.getElementById('generateBtn');
const resetBtn = document.getElementById('resetBtn');
const copyBtn = document.getElementById('copyBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMessage = document.getElementById('errorMessage');
const outputContent = document.getElementById('outputContent');

// Form fields
const techniqueSelect = document.getElementById('technique');
const businessAreaSelect = document.getElementById('business_area');
const iconSelect = document.getElementById('icon');
const issueTextarea = document.getElementById('issue');
const assumptionsTextarea = document.getElementById('assumptions');

// Event Listeners
form.addEventListener('submit', handleFormSubmit);
resetBtn.addEventListener('click', handleReset);
copyBtn.addEventListener('click', handleCopy);

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Validate required fields
    if (!techniqueSelect.value || !issueTextarea.value.trim()) {
        showError('Please fill in all required fields (Technique and Issue).');
        return;
    }
    
    // Prepare data
    const formData = {
        technique: techniqueSelect.value,
        business_area: businessAreaSelect.value,
        icon: iconSelect.value,
        issue: issueTextarea.value.trim(),
        assumptions: assumptionsTextarea.value.trim()
    };
    
    // Show loading state
    setLoadingState(true);
    hideError();
    
    try {
        // Make API call
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Display the output
            displayOutput(data.output);
            copyBtn.style.display = 'inline-block';
        } else {
            // Show error
            showError(data.error || 'An error occurred while generating content.');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Network error. Please check your connection and try again.');
    } finally {
        setLoadingState(false);
    }
}

/**
 * Display the generated output
 */
function displayOutput(markdownText) {
    // Convert markdown to HTML (simple conversion)
    const htmlContent = convertMarkdownToHTML(markdownText);
    outputContent.innerHTML = htmlContent;
    
    // Scroll to output section
    document.getElementById('outputSection').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
}

/**
 * Simple markdown to HTML converter
 */
function convertMarkdownToHTML(markdown) {
    let html = markdown;
    
    // Headers
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    
    // Bold
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');
    
    // Italic
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    html = html.replace(/_(.*?)_/g, '<em>$1</em>');
    
    // Unordered lists
    html = html.replace(/^\* (.+)$/gim, '<li>$1</li>');
    html = html.replace(/^- (.+)$/gim, '<li>$1</li>');
    
    // Ordered lists
    html = html.replace(/^\d+\. (.+)$/gim, '<li>$1</li>');
    
    // Wrap consecutive list items in ul/ol
    html = html.replace(/(<li>.*<\/li>)/s, function(match) {
        return '<ul>' + match + '</ul>';
    });
    
    // Code blocks
    html = html.replace(/```(.*?)```/gs, '<pre><code>$1</code></pre>');
    
    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Line breaks
    html = html.replace(/\n\n/g, '</p><p>');
    html = '<p>' + html + '</p>';
    
    // Clean up empty paragraphs
    html = html.replace(/<p><\/p>/g, '');
    html = html.replace(/<p>(<h[1-6]>)/g, '$1');
    html = html.replace(/(<\/h[1-6]>)<\/p>/g, '$1');
    html = html.replace(/<p>(<ul>)/g, '$1');
    html = html.replace(/(<\/ul>)<\/p>/g, '$1');
    html = html.replace(/<p>(<ol>)/g, '$1');
    html = html.replace(/(<\/ol>)<\/p>/g, '$1');
    
    return html;
}

/**
 * Handle reset button click
 */
function handleReset() {
    form.reset();
    outputContent.innerHTML = '';
    copyBtn.style.display = 'none';
    hideError();
}

/**
 * Handle copy to clipboard
 */
function handleCopy() {
    const textContent = outputContent.innerText;
    
    navigator.clipboard.writeText(textContent).then(() => {
        // Change button text temporarily
        const originalText = copyBtn.textContent;
        copyBtn.textContent = 'Copied!';
        copyBtn.style.backgroundColor = '#2ecc40';
        
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.backgroundColor = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        showError('Failed to copy to clipboard.');
    });
}

/**
 * Set loading state
 */
function setLoadingState(isLoading) {
    if (isLoading) {
        loadingSpinner.style.display = 'block';
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
        outputContent.innerHTML = '';
        copyBtn.style.display = 'none';
    } else {
        loadingSpinner.style.display = 'none';
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate Analysis';
    }
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

/**
 * Hide error message
 */
function hideError() {
    errorMessage.style.display = 'none';
    errorMessage.textContent = '';
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Spana application initialized');
});

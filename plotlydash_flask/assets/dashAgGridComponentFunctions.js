// ------------------------------------------------------------------------------------------------------------
//How this Function works:
//
// The code creates a custom renderer function, Highlight, for use within an ag-Grid table. 
// This function specifically targets text wrapped in <span> tags within cells and styles them with a green color.
// 
//  - Since there is no search keyword in the props, i have to First  wrap the keyword
//    in span tags in Callback then
//  - i have to again remove and reconstruct that in createElement, this is needed for AG Grid
//    otherwise the styling doesnot work.
//  - then the text before and after the span is extracted and inserted into final creteElement  
//--------------------------------------------------------------------------------------------------------------


// This line ensures that a global object dashAgGridComponentFunctions exists. If it doesn't, it creates an empty object
var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};


// Defines a function named highlightKeywordRenderer and assigns it as a property called Highlight to the dagcomponentfuncs object
dagcomponentfuncs.Highlight = function highlightKeywordRenderer(props) {
    const cellValue = props.value;                                  //  it retrieves the value of the current cell
    const spanMatches = cellValue.matchAll(/<span>(.*?)<\/span>/g); // Use matchAll with 'g' flag
    
    if (spanMatches) {
        let result = []; // Array to store fragments
        let lastIndex = 0;
        
        // The code iterates through each matched span
        for (const match of spanMatches) {
            // The following line effectively extracts the text from the cellValue:
            // - Starting Point (lastIndex): It starts extracting from the position after the end of the previous span
            // - Ending Point (match.index): It extracts text up to, but not including, the start of the current span.
            const beforeSpan = cellValue.substring(lastIndex, match.index);
            const spanText = match[1];        // This refers to the first capture group you defined in your regular expression
            const styledSpan = React.createElement('span', { style: { color: 'green' } }, spanText);

            result.push(beforeSpan); // Add text before span
            result.push(styledSpan); // Add styled span
            lastIndex = match.index + match[0].length; // Update lastIndex
        }

        // Add remaining text after the last span
        result.push(cellValue.substring(lastIndex));

        // Return a fragment containing all parts
        //Fragments provide a way to group multiple elements without adding extra nodes to the DOM
        //
        // The spread syntax (...) takes all the elements (plain text strings and styled <span> elements) 
        // in the result array and passes them as individual children to the React.Fragment.
        return React.createElement(React.Fragment, null, ...result);
    } else {
        // If no spans found, return the original cell value
        return cellValue;
    }
}

   
    
    
    
    
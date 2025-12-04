
window.setDotNetReference = function(dotNetRef) {
    window.dotNetRef = dotNetRef;
    console.log('DotNet reference set');
}

async function stateColorCallback(stateid) {
    // Store the state click for later retrieval by Blazor
    window.lastClickedState = stateid;
    const result = await dotNetRef.invokeMethodAsync('OnStateClicked', stateid);
    console.log(`State ${stateid} colored with result: ${result}`);
}



// Wait for the SVG object to load before accessing its content
window.initializeMap = function (map) {
    console.log("attempting to load map" + map);
    const obj = document.querySelector(map);
    
    if (!obj) {
        console.log('SVG object element not found, retrying...');
        setTimeout(initializeMap, 100);
        return;
    }
    
    console.log('Found SVG object, waiting for load...');
    
    // Wait for the SVG to load
    obj.addEventListener('load', function() {
        const svgDoc = obj.contentDocument;
        
        if (!svgDoc) {
            console.error('Could not access SVG content document');
            return;
        }
        
        console.log('SVG loaded successfully');
        
        // Get all state paths in the SVG
        states = svgDoc.querySelectorAll('path, polygon, circle, rect'); // Common SVG elements for states
        
        console.log(`Found ${states.length} potential state elements`);
        
        // Add mouse event listeners to each state
        states.forEach(function(state) {
            // Color state on mouse hover
            state.addEventListener('mouseenter', function() {
                // Store original color if not already stored
                if (!state.dataset.originalFill) {
                    state.dataset.originalFill = state.style.fill || state.getAttribute('fill') || '#cccccc';
                }
                
                // Change to hover color
                state.style.fill = 'lightblue';
                
                // Log which state is being hovered (if it has an id)
                if (state.id) {
                    console.log(`Hovering over state: ${state.id}`);
                }
            });
            
            // Restore original color when mouse leaves
            state.addEventListener('mouseleave', function() {
                if (state.dataset.originalFill) {
                    state.style.fill = state.dataset.originalFill;
                }
            });

            // Click to color state with selected color
            state.addEventListener('click', function() {
                    stateColorCallback(state.id);
                    
                    if (state.id) {
                        console.log(`Clicked state ${state.id}`);
                    }

            });
        });
    });
}
window.setSelectedColor = function(color) {
	selectedColor = color;
	console.log(`Selected color set to ${color}`);
}


window.colorState = function(stateId, color) {
    if (!states) {
        console.error('States not loaded yet');
        return false;
    }
    
    // Find the state element by ID
    let targetState = null;
    states.forEach(function(state) {
        if (state.id === stateId) {
            targetState = state;
        }
    });
    
    if (!targetState) {
        console.error(`State with ID '${stateId}' not found`);
        return false;
    }
    
    // Color the state
    targetState.style.fill = color;
    targetState.dataset.originalFill = color; // Update stored color
    
    console.log(`Colored state ${stateId} with ${color}`);
    return true;
}


window.getLastClickedState = function() {
    const state = window.lastClickedState;
    window.lastClickedState = null; 
    return state;
}

/*
function waitForBlazor() {
    if (window.Blazor && window.Blazor.start) {
        setTimeout(initializeMap, 500);
    } else {
        setTimeout(waitForBlazor, 100);
    }
}

waitForBlazor();
*/

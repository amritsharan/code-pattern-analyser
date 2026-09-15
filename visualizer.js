/**
 * Interactive Algorithm Step-by-Step Visualizer
 * Supports Two Pointers, Sliding Window, Binary Search, and Monotonic Stack simulations.
 */

class AlgorithmSimulator {
    constructor() {
        this.currentPattern = 'two_pointers';
        this.steps = [];
        this.currentStepIndex = 0;
        this.isPlaying = false;
        this.playInterval = null;
        this.speed = 1000; // ms per step
        this.customData = null;
    }

    init(patternKey, customInput = null) {
        this.currentPattern = patternKey;
        this.pause();
        this.currentStepIndex = 0;
        this.customData = customInput;
        this.generateSteps();
        this.render();
    }

    generateSteps() {
        this.steps = [];
        switch (this.currentPattern) {
            case 'two_pointers':
                this.generateTwoPointersSteps();
                break;
            case 'sliding_window':
                this.generateSlidingWindowSteps();
                break;
            case 'binary_search':
                this.generateBinarySearchSteps();
                break;
            case 'monotonic_stack':
                this.generateMonotonicStackSteps();
                break;
            default:
                this.generateGenericSteps();
                break;
        }
    }

    // --- 1. Two Pointers Simulation (e.g. Two Sum on Sorted Array) ---
    generateTwoPointersSteps() {
        let arr = [1, 2, 4, 7, 11, 15, 18];
        let target = 18;

        if (this.customData && Array.isArray(this.customData.arr) && this.customData.arr.length >= 2) {
            arr = [...this.customData.arr].sort((a, b) => a - b);
            if (this.customData.target !== undefined) target = Number(this.customData.target);
        }

        let left = 0;
        let right = arr.length - 1;

        this.steps.push({
            type: 'two_pointers',
            arr: [...arr],
            left,
            right,
            target,
            currentSum: arr[left] + arr[right],
            status: 'initial',
            message: `Initialize left pointer at index 0 (${arr[left]}) and right pointer at index ${right} (${arr[right]}). Target sum = ${target}.`
        });

        while (left < right) {
            const sum = arr[left] + arr[right];
            if (sum === target) {
                this.steps.push({
                    type: 'two_pointers',
                    arr: [...arr],
                    left,
                    right,
                    target,
                    currentSum: sum,
                    status: 'found',
                    message: `🎯 Target found! arr[${left}] (${arr[left]}) + arr[${right}] (${arr[right]}) = ${sum} matches target ${target}.`
                });
                return;
            } else if (sum < target) {
                this.steps.push({
                    type: 'two_pointers',
                    arr: [...arr],
                    left,
                    right,
                    target,
                    currentSum: sum,
                    status: 'move_left',
                    message: `Current sum ${sum} < target ${target}. Increment left pointer from index ${left} to ${left + 1} to increase sum.`
                });
                left++;
            } else {
                this.steps.push({
                    type: 'two_pointers',
                    arr: [...arr],
                    left,
                    right,
                    target,
                    currentSum: sum,
                    status: 'move_right',
                    message: `Current sum ${sum} > target ${target}. Decrement right pointer from index ${right} to ${right - 1} to decrease sum.`
                });
                right--;
            }
        }

        this.steps.push({
            type: 'two_pointers',
            arr: [...arr],
            left,
            right,
            target,
            currentSum: null,
            status: 'not_found',
            message: `Left and right pointers crossed. No pair exists with sum = ${target}.`
        });
    }

    // --- 2. Sliding Window Simulation (Max sum subarray of size k) ---
    generateSlidingWindowSteps() {
        let arr = [2, 1, 5, 1, 3, 2, 6];
        let k = 3;

        if (this.customData && Array.isArray(this.customData.arr) && this.customData.arr.length >= 3) {
            arr = [...this.customData.arr];
            if (this.customData.k !== undefined) k = Math.min(Number(this.customData.k), arr.length);
        }

        let left = 0;
        let currentSum = 0;
        let maxSum = 0;

        for (let right = 0; right < arr.length; right++) {
            currentSum += arr[right];

            if (right < k - 1) {
                this.steps.push({
                    type: 'sliding_window',
                    arr: [...arr],
                    left: 0,
                    right,
                    k,
                    currentSum,
                    maxSum: currentSum,
                    status: 'building',
                    message: `Building initial window: added arr[${right}] (${arr[right]}). Window sum = ${currentSum}.`
                });
            } else {
                if (right === k - 1) {
                    maxSum = currentSum;
                } else {
                    currentSum -= arr[left];
                    left++;
                    maxSum = Math.max(maxSum, currentSum);
                }

                this.steps.push({
                    type: 'sliding_window',
                    arr: [...arr],
                    left,
                    right,
                    k,
                    currentSum,
                    maxSum,
                    status: 'sliding',
                    message: `Window [${left}..${right}] elements: [${arr.slice(left, right + 1).join(', ')}]. Window sum = ${currentSum}, Max sum so far = ${maxSum}.`
                });
            }
        }

        this.steps.push({
            type: 'sliding_window',
            arr: [...arr],
            left,
            right: arr.length - 1,
            k,
            currentSum,
            maxSum,
            status: 'done',
            message: `✅ Sliding window complete! Maximum subarray sum of size ${k} is ${maxSum}.`
        });
    }

    // --- 3. Binary Search Simulation ---
    generateBinarySearchSteps() {
        let arr = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91];
        let target = 23;

        if (this.customData && Array.isArray(this.customData.arr)) {
            arr = [...this.customData.arr].sort((a, b) => a - b);
            if (this.customData.target !== undefined) target = Number(this.customData.target);
        }

        let low = 0;
        let high = arr.length - 1;

        this.steps.push({
            type: 'binary_search',
            arr: [...arr],
            low,
            high,
            mid: Math.floor((low + high) / 2),
            target,
            status: 'initial',
            message: `Search range [${low}..${high}], target = ${target}. Computing mid index...`
        });

        while (low <= high) {
            const mid = Math.floor(low + (high - low) / 2);
            const midVal = arr[mid];

            if (midVal === target) {
                this.steps.push({
                    type: 'binary_search',
                    arr: [...arr],
                    low,
                    high,
                    mid,
                    target,
                    status: 'found',
                    message: `🎯 Target ${target} found at index ${mid} (arr[${mid}] == ${target})!`
                });
                return;
            } else if (midVal < target) {
                this.steps.push({
                    type: 'binary_search',
                    arr: [...arr],
                    low,
                    high,
                    mid,
                    target,
                    status: 'search_right',
                    message: `arr[${mid}] (${midVal}) < target (${target}). Discarding left half [${low}..${mid}]. Updating low = ${mid + 1}.`
                });
                low = mid + 1;
            } else {
                this.steps.push({
                    type: 'binary_search',
                    arr: [...arr],
                    low,
                    high,
                    mid,
                    target,
                    status: 'search_left',
                    message: `arr[${mid}] (${midVal}) > target (${target}). Discarding right half [${mid}..${high}]. Updating high = ${mid - 1}.`
                });
                high = mid - 1;
            }
        }

        this.steps.push({
            type: 'binary_search',
            arr: [...arr],
            low,
            high,
            mid: -1,
            target,
            status: 'not_found',
            message: `Search bounds crossed (low > high). Target ${target} not present in array.`
        });
    }

    // --- 4. Monotonic Stack Simulation (Next Greater Element) ---
    generateMonotonicStackSteps() {
        let arr = [4, 5, 2, 10, 8];
        if (this.customData && Array.isArray(this.customData.arr) && this.customData.arr.length > 0) {
            arr = [...this.customData.arr];
        }

        const stack = []; // will store indices
        const result = new Array(arr.length).fill(-1);

        this.steps.push({
            type: 'monotonic_stack',
            arr: [...arr],
            currentIndex: -1,
            stack: [],
            result: [...result],
            message: 'Initialize empty monotonic decreasing stack and result array with -1.'
        });

        for (let i = 0; i < arr.length; i++) {
            const currentVal = arr[i];

            while (stack.length > 0 && arr[stack[stack.length - 1]] < currentVal) {
                const poppedIdx = stack.pop();
                result[poppedIdx] = currentVal;
                this.steps.push({
                    type: 'monotonic_stack',
                    arr: [...arr],
                    currentIndex: i,
                    stack: [...stack],
                    result: [...result],
                    poppedIndex: poppedIdx,
                    message: `arr[${i}] (${currentVal}) > stack top arr[${poppedIdx}] (${arr[poppedIdx]}). Popped index ${poppedIdx}, set next greater to ${currentVal}.`
                });
            }

            stack.push(i);
            this.steps.push({
                type: 'monotonic_stack',
                arr: [...arr],
                currentIndex: i,
                stack: [...stack],
                result: [...result],
                message: `Pushed index ${i} (value ${currentVal}) onto monotonic stack.`
            });
        }

        this.steps.push({
            type: 'monotonic_stack',
            arr: [...arr],
            currentIndex: arr.length,
            stack: [...stack],
            result: [...result],
            message: `✅ Monotonic stack traversal complete. Final next greater elements: [${result.join(', ')}].`
        });
    }

    // --- Generic Pattern Fallback Simulator ---
    generateGenericSteps() {
        this.steps.push({
            type: 'generic',
            message: `Interactive step-by-step simulator configured for ${this.currentPattern.replace('_', ' ').toUpperCase()}. Click Next Step to step through algorithmic stages.`
        });
        this.steps.push({
            type: 'generic',
            message: `Step 1: Input data validation and state initialization.`
        });
        this.steps.push({
            type: 'generic',
            message: `Step 2: Subproblem transition / invariant maintenance in progress.`
        });
        this.steps.push({
            type: 'generic',
            message: `Step 3: Optimal state reached and solution synthesized.`
        });
    }

    // --- Step Navigation Controls ---
    nextStep() {
        if (this.currentStepIndex < this.steps.length - 1) {
            this.currentStepIndex++;
            this.render();
        } else {
            this.pause();
        }
    }

    prevStep() {
        if (this.currentStepIndex > 0) {
            this.currentStepIndex--;
            this.render();
        }
    }

    reset() {
        this.pause();
        this.currentStepIndex = 0;
        this.render();
    }

    togglePlay() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }

    play() {
        if (this.currentStepIndex >= this.steps.length - 1) {
            this.currentStepIndex = 0;
        }
        this.isPlaying = true;
        this.updatePlayButtonUI();
        this.playInterval = setInterval(() => {
            if (this.currentStepIndex < this.steps.length - 1) {
                this.nextStep();
            } else {
                this.pause();
            }
        }, this.speed);
    }

    pause() {
        this.isPlaying = false;
        if (this.playInterval) {
            clearInterval(this.playInterval);
            this.playInterval = null;
        }
        this.updatePlayButtonUI();
    }

    setSpeed(speedMs) {
        this.speed = speedMs;
        if (this.isPlaying) {
            this.pause();
            this.play();
        }
    }

    updatePlayButtonUI() {
        const btn = document.getElementById('sim-play-btn');
        if (btn) {
            btn.innerHTML = this.isPlaying ? '⏸️ Pause' : '▶️ Auto-Play';
        }
    }

    // --- DOM Rendering Engine ---
    render() {
        const container = document.getElementById('simulator-canvas-container');
        if (!container) return;

        const step = this.steps[this.currentStepIndex] || {};
        const stepNum = this.currentStepIndex + 1;
        const totalSteps = this.steps.length;

        // Progress label
        const progressEl = document.getElementById('sim-step-indicator');
        if (progressEl) {
            progressEl.innerText = `Step ${stepNum} of ${totalSteps}`;
        }

        // Message log
        const logEl = document.getElementById('sim-log-message');
        if (logEl) {
            logEl.innerHTML = step.message || 'Ready.';
        }

        // Render visual elements based on step type
        let canvasHtml = '';

        if (step.type === 'two_pointers') {
            canvasHtml = this.renderTwoPointersHTML(step);
        } else if (step.type === 'sliding_window') {
            canvasHtml = this.renderSlidingWindowHTML(step);
        } else if (step.type === 'binary_search') {
            canvasHtml = this.renderBinarySearchHTML(step);
        } else if (step.type === 'monotonic_stack') {
            canvasHtml = this.renderMonotonicStackHTML(step);
        } else {
            canvasHtml = `<div class="generic-sim-box"><p>${step.message || 'Simulation in progress'}</p></div>`;
        }

        container.innerHTML = canvasHtml;
    }

    renderTwoPointersHTML(step) {
        let cells = '';
        step.arr.forEach((val, idx) => {
            const isLeft = idx === step.left;
            const isRight = idx === step.right;
            let classes = 'sim-cell';
            if (step.status === 'found' && (isLeft || isRight)) classes += ' match';
            else if (isLeft && isRight) classes += ' pointer-both';
            else if (isLeft) classes += ' pointer-left';
            else if (isRight) classes += ' pointer-right';

            cells += `
                <div class="${classes}">
                    <span class="cell-val">${val}</span>
                    <span class="cell-idx">[${idx}]</span>
                    ${isLeft ? '<span class="pointer-tag tag-left">L</span>' : ''}
                    ${isRight ? '<span class="pointer-tag tag-right">R</span>' : ''}
                </div>
            `;
        });

        return `
            <div class="sim-visual-row">
                <div class="sim-array-wrapper">${cells}</div>
                <div class="sim-stats-pill">
                    <span>Target: <strong>${step.target}</strong></span>
                    ${step.currentSum !== null ? `<span>Current Sum: <strong>${step.currentSum}</strong></span>` : ''}
                </div>
            </div>
        `;
    }

    renderSlidingWindowHTML(step) {
        let cells = '';
        step.arr.forEach((val, idx) => {
            const inWindow = idx >= step.left && idx <= step.right;
            let classes = 'sim-cell';
            if (inWindow) classes += ' in-window';
            if (idx === step.left) classes += ' window-start';
            if (idx === step.right) classes += ' window-end';

            cells += `
                <div class="${classes}">
                    <span class="cell-val">${val}</span>
                    <span class="cell-idx">[${idx}]</span>
                    ${idx === step.left ? '<span class="pointer-tag tag-left">L</span>' : ''}
                    ${idx === step.right ? '<span class="pointer-tag tag-right">R</span>' : ''}
                </div>
            `;
        });

        return `
            <div class="sim-visual-row">
                <div class="sim-array-wrapper">${cells}</div>
                <div class="sim-stats-pill">
                    <span>Window Size K: <strong>${step.k}</strong></span>
                    <span>Window Sum: <strong>${step.currentSum}</strong></span>
                    <span>Max Sum: <strong style="color:#3fb950;">${step.maxSum}</strong></span>
                </div>
            </div>
        `;
    }

    renderBinarySearchHTML(step) {
        let cells = '';
        step.arr.forEach((val, idx) => {
            const isEliminated = idx < step.low || idx > step.high;
            const isMid = idx === step.mid;
            const isLow = idx === step.low;
            const isHigh = idx === step.high;
            
            let classes = 'sim-cell';
            if (isEliminated) classes += ' eliminated';
            if (isMid && step.status === 'found') classes += ' match';
            else if (isMid) classes += ' mid-cell';

            cells += `
                <div class="${classes}">
                    <span class="cell-val">${val}</span>
                    <span class="cell-idx">[${idx}]</span>
                    ${isMid ? '<span class="pointer-tag tag-mid">MID</span>' : ''}
                    ${isLow && !isMid ? '<span class="pointer-tag tag-left">LOW</span>' : ''}
                    ${isHigh && !isMid ? '<span class="pointer-tag tag-right">HIGH</span>' : ''}
                </div>
            `;
        });

        return `
            <div class="sim-visual-row">
                <div class="sim-array-wrapper">${cells}</div>
                <div class="sim-stats-pill">
                    <span>Target: <strong>${step.target}</strong></span>
                    <span>Range: <strong>[${step.low}..${step.high}]</strong></span>
                    ${step.mid >= 0 ? `<span>Mid Index: <strong>${step.mid} (${step.arr[step.mid]})</strong></span>` : ''}
                </div>
            </div>
        `;
    }

    renderMonotonicStackHTML(step) {
        let arrCells = '';
        step.arr.forEach((val, idx) => {
            const isCurrent = idx === step.currentIndex;
            const inStack = step.stack.includes(idx);
            let classes = 'sim-cell';
            if (isCurrent) classes += ' current-cell';
            else if (inStack) classes += ' in-stack-cell';

            arrCells += `
                <div class="${classes}">
                    <span class="cell-val">${val}</span>
                    <span class="cell-idx">[${idx}]</span>
                    <span class="nge-val">NGE: ${step.result[idx]}</span>
                </div>
            `;
        });

        let stackItems = '';
        if (step.stack.length === 0) {
            stackItems = '<div class="stack-empty-msg">Empty Stack</div>';
        } else {
            step.stack.forEach(idx => {
                stackItems = `<div class="stack-box-item"><span class="idx-tag">[${idx}]</span> <strong>${step.arr[idx]}</strong></div>` + stackItems;
            });
        }

        return `
            <div class="sim-visual-split">
                <div class="sim-array-side">
                    <h4>Input Elements & Next Greater Element Array</h4>
                    <div class="sim-array-wrapper">${arrCells}</div>
                </div>
                <div class="sim-stack-side">
                    <h4>Monotonic Stack (Indices & Values)</h4>
                    <div class="stack-visual-container">${stackItems}</div>
                </div>
            </div>
        `;
    }
}

// Global Simulator Instance
window.dsaSimulator = new AlgorithmSimulator();

window.initVisualizerForPattern = function(patternKey) {
    if (window.dsaSimulator) {
        window.dsaSimulator.init(patternKey);
    }
};

window.applyCustomSimInput = function() {
    const inputEl = document.getElementById('sim-custom-input');
    const targetEl = document.getElementById('sim-custom-target');
    if (!inputEl) return;

    const raw = inputEl.value.trim();
    if (!raw) return;

    try {
        const arr = raw.split(',').map(s => Number(s.trim())).filter(n => !isNaN(n));
        const target = targetEl ? Number(targetEl.value.trim()) : 10;

        if (arr.length > 0) {
            window.dsaSimulator.init(window.dsaSimulator.currentPattern, { arr, target, k: target });
        }
    } catch (e) {
        alert('Invalid input format. Use comma separated numbers like: 2, 7, 11, 15');
    }
};

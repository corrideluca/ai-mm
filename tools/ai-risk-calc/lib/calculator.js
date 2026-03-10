'use strict';

/**
 * Core position sizing calculations.
 * No dependencies — pure math.
 */

/**
 * Calculate position size based on risk percentage and stop loss.
 *
 * @param {object} params
 * @param {number} params.balance      - Total portfolio balance
 * @param {number} params.riskPercent  - Risk per trade as percentage (e.g. 2 for 2%)
 * @param {number} params.maxPosition  - Max position as percentage of balance (e.g. 20 for 20%)
 * @param {number} params.entry        - Entry price
 * @param {number} params.stop         - Stop loss price
 * @param {number} [params.target]     - Optional target/take-profit price
 * @returns {object} Calculated position details
 */
function calculatePosition(params) {
  const { balance, riskPercent, maxPosition, entry, stop, target } = params;

  // Validate inputs
  if (balance <= 0) throw new Error('Balance must be positive');
  if (riskPercent <= 0 || riskPercent > 100) throw new Error('Risk % must be between 0 and 100');
  if (maxPosition <= 0 || maxPosition > 100) throw new Error('Max position % must be between 0 and 100');
  if (entry <= 0) throw new Error('Entry price must be positive');
  if (stop <= 0) throw new Error('Stop loss price must be positive');
  if (entry === stop) throw new Error('Entry and stop loss cannot be the same');

  const isLong = entry > stop;
  const direction = isLong ? 'LONG' : 'SHORT';

  // Dollar risk per trade
  const dollarRisk = balance * (riskPercent / 100);

  // Risk per share (distance from entry to stop)
  const riskPerShare = Math.abs(entry - stop);

  // Position size in shares (based on risk)
  let shares = dollarRisk / riskPerShare;

  // Position value
  let positionValue = shares * entry;

  // Max position cap
  const maxPositionValue = balance * (maxPosition / 100);
  let capped = false;
  if (positionValue > maxPositionValue) {
    positionValue = maxPositionValue;
    shares = positionValue / entry;
    capped = true;
  }

  // Actual dollar at risk (may be less if capped)
  const actualDollarRisk = shares * riskPerShare;
  const actualRiskPercent = (actualDollarRisk / balance) * 100;

  // Position as percentage of balance
  const positionPercent = (positionValue / balance) * 100;

  const result = {
    direction,
    shares: roundTo(shares, 4),
    positionValue: roundTo(positionValue, 2),
    positionPercent: roundTo(positionPercent, 2),
    dollarRisk: roundTo(actualDollarRisk, 2),
    riskPercent: roundTo(actualRiskPercent, 2),
    riskPerShare: roundTo(riskPerShare, 4),
    entry,
    stop,
    capped,
  };

  // Reward:Risk ratio if target provided
  if (target !== undefined && target !== null) {
    if (target <= 0) throw new Error('Target price must be positive');

    const rewardPerShare = Math.abs(target - entry);
    const rewardRiskRatio = rewardPerShare / riskPerShare;
    const potentialProfit = shares * rewardPerShare;

    result.target = target;
    result.rewardPerShare = roundTo(rewardPerShare, 4);
    result.rewardRiskRatio = roundTo(rewardRiskRatio, 2);
    result.potentialProfit = roundTo(potentialProfit, 2);
    result.potentialProfitPercent = roundTo((potentialProfit / balance) * 100, 2);
  }

  return result;
}

/**
 * Kelly Criterion — optimal bet sizing for repeated bets.
 *
 * Formula: f* = (p * b - q) / b
 *   where p = win probability, q = 1 - p, b = avg_win / avg_loss
 *
 * @param {object} params
 * @param {number} params.balance  - Total balance
 * @param {number} params.winRate  - Win rate as decimal (e.g. 0.6 for 60%)
 * @param {number} params.avgWin   - Average win amount (or multiplier)
 * @param {number} params.avgLoss  - Average loss amount (or multiplier)
 * @returns {object} Kelly calculation results
 */
function calculateKelly(params) {
  const { balance, winRate, avgWin, avgLoss } = params;

  if (balance <= 0) throw new Error('Balance must be positive');
  if (winRate <= 0 || winRate >= 1) throw new Error('Win rate must be between 0 and 1 (exclusive)');
  if (avgWin <= 0) throw new Error('Average win must be positive');
  if (avgLoss <= 0) throw new Error('Average loss must be positive');

  const p = winRate;
  const q = 1 - p;
  const b = avgWin / avgLoss;

  // Full Kelly
  const fullKelly = (p * b - q) / b;

  // Half Kelly (more conservative, commonly used)
  const halfKelly = fullKelly / 2;

  // Quarter Kelly (very conservative)
  const quarterKelly = fullKelly / 4;

  // Expected value per dollar risked
  const expectedValue = (p * avgWin) - (q * avgLoss);

  // Edge percentage
  const edge = expectedValue / avgLoss;

  return {
    fullKelly: roundTo(Math.max(0, fullKelly) * 100, 2),
    halfKelly: roundTo(Math.max(0, halfKelly) * 100, 2),
    quarterKelly: roundTo(Math.max(0, quarterKelly) * 100, 2),
    fullKellyAmount: roundTo(Math.max(0, fullKelly) * balance, 2),
    halfKellyAmount: roundTo(Math.max(0, halfKelly) * balance, 2),
    quarterKellyAmount: roundTo(Math.max(0, quarterKelly) * balance, 2),
    expectedValue: roundTo(expectedValue, 4),
    edge: roundTo(edge * 100, 2),
    winRate: roundTo(winRate * 100, 2),
    avgWin,
    avgLoss,
    hasEdge: fullKelly > 0,
  };
}

/**
 * Quick risk/reward summary for a given balance and risk %.
 * Useful when you don't have specific entry/stop yet.
 *
 * @param {number} balance
 * @param {number} riskPercent
 * @param {number} maxPosition
 * @returns {object}
 */
function quickSummary(balance, riskPercent, maxPosition) {
  return {
    balance: roundTo(balance, 2),
    riskPerTrade: roundTo(balance * (riskPercent / 100), 2),
    riskPercent: roundTo(riskPercent, 2),
    maxPositionValue: roundTo(balance * (maxPosition / 100), 2),
    maxPositionPercent: roundTo(maxPosition, 2),
    // Common R:R targets
    targets: {
      '1R': roundTo(balance * (riskPercent / 100) * 1, 2),
      '2R': roundTo(balance * (riskPercent / 100) * 2, 2),
      '3R': roundTo(balance * (riskPercent / 100) * 3, 2),
      '5R': roundTo(balance * (riskPercent / 100) * 5, 2),
    },
  };
}

function roundTo(num, decimals) {
  const factor = Math.pow(10, decimals);
  return Math.round(num * factor) / factor;
}

module.exports = { calculatePosition, calculateKelly, quickSummary };

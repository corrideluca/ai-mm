#!/usr/bin/env node
'use strict';

const readline = require('readline');
const { calculatePosition, calculateKelly, quickSummary } = require('./lib/calculator');

// ── ANSI color helpers (zero dependencies) ──────────────────────────────────
const c = {
  reset:   '\x1b[0m',
  bold:    '\x1b[1m',
  dim:     '\x1b[2m',
  red:     '\x1b[31m',
  green:   '\x1b[32m',
  yellow:  '\x1b[33m',
  blue:    '\x1b[34m',
  magenta: '\x1b[35m',
  cyan:    '\x1b[36m',
  white:   '\x1b[37m',
  bgBlue:  '\x1b[44m',
};

const paint = (color, text) => `${color}${text}${c.reset}`;
const bold  = (text) => paint(c.bold, text);
const dim   = (text) => paint(c.dim, text);
const green = (text) => paint(c.green, text);
const red   = (text) => paint(c.red, text);
const cyan  = (text) => paint(c.cyan, text);
const yellow = (text) => paint(c.yellow, text);
const magenta = (text) => paint(c.magenta, text);
const blue  = (text) => paint(c.blue, text);

// ── Argument parsing (no deps) ──────────────────────────────────────────────
function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      // Boolean flags (no value following, or next arg is also a flag)
      if (!next || next.startsWith('--')) {
        args[key] = true;
      } else {
        args[key] = next;
        i++;
      }
    } else if (arg === '-h') {
      args.help = true;
    } else if (arg === '-v') {
      args.version = true;
    }
  }
  return args;
}

// ── Display functions ───────────────────────────────────────────────────────
function banner() {
  console.log('');
  console.log(cyan('  ╔══════════════════════════════════════╗'));
  console.log(cyan('  ║') + bold('   ai-risk-calc ') + dim('v1.0.0') + cyan('               ║'));
  console.log(cyan('  ║') + dim('   Position Sizing Calculator') + cyan('         ║'));
  console.log(cyan('  ╚══════════════════════════════════════╝'));
  console.log('');
}

function separator() {
  console.log(dim('  ─────────────────────────────────────'));
}

function displayPosition(result) {
  banner();

  const dirColor = result.direction === 'LONG' ? green : red;

  console.log(bold('  POSITION SIZING'));
  separator();
  console.log(`  Direction:        ${dirColor(result.direction)}`);
  console.log(`  Entry Price:      ${bold('$' + result.entry)}`);
  console.log(`  Stop Loss:        ${red('$' + result.stop)}`);
  if (result.target) {
    console.log(`  Target Price:     ${green('$' + result.target)}`);
  }
  separator();
  console.log(`  Shares/Units:     ${bold(result.shares.toString())}`);
  console.log(`  Position Value:   ${bold('$' + result.positionValue)}  ${dim('(' + result.positionPercent + '% of balance)')}`);
  console.log(`  Dollar at Risk:   ${yellow('$' + result.dollarRisk)}  ${dim('(' + result.riskPercent + '% of balance)')}`);
  console.log(`  Risk per Share:   ${dim('$' + result.riskPerShare)}`);

  if (result.capped) {
    console.log('');
    console.log(yellow('  ! Position capped at max position limit'));
  }

  if (result.rewardRiskRatio !== undefined) {
    console.log('');
    console.log(bold('  REWARD : RISK'));
    separator();
    const rrColor = result.rewardRiskRatio >= 2 ? green : result.rewardRiskRatio >= 1 ? yellow : red;
    console.log(`  R:R Ratio:        ${rrColor(result.rewardRiskRatio + ':1')}`);
    console.log(`  Potential Profit: ${green('+$' + result.potentialProfit)}  ${dim('(' + result.potentialProfitPercent + '% of balance)')}`);

    if (result.rewardRiskRatio < 1) {
      console.log(red('  ! Risk exceeds reward. Consider adjusting your trade.'));
    } else if (result.rewardRiskRatio >= 3) {
      console.log(green('  * Excellent risk/reward setup'));
    }
  }

  console.log('');
}

function displayKelly(result) {
  banner();

  console.log(bold('  KELLY CRITERION'));
  separator();
  console.log(`  Win Rate:         ${bold(result.winRate + '%')}`);
  console.log(`  Avg Win:          ${green(result.avgWin.toString())}`);
  console.log(`  Avg Loss:         ${red(result.avgLoss.toString())}`);
  console.log(`  Edge:             ${result.hasEdge ? green(result.edge + '%') : red(result.edge + '%')}`);
  console.log(`  Expected Value:   ${result.expectedValue >= 0 ? green(result.expectedValue.toString()) : red(result.expectedValue.toString())}  ${dim('per dollar risked')}`);
  separator();

  if (!result.hasEdge) {
    console.log('');
    console.log(red('  NO EDGE DETECTED - Kelly says don\'t bet!'));
    console.log(red('  Your expected value is negative.'));
    console.log('');
    return;
  }

  console.log('');
  console.log(bold('  RECOMMENDED SIZING'));
  separator();
  console.log(`  Full Kelly:       ${yellow(result.fullKelly + '%')}  ${dim('= $' + result.fullKellyAmount)}  ${dim('(aggressive)')}`);
  console.log(`  Half Kelly:       ${green(result.halfKelly + '%')}  ${dim('= $' + result.halfKellyAmount)}  ${dim('(recommended)')}`);
  console.log(`  Quarter Kelly:    ${cyan(result.quarterKelly + '%')}  ${dim('= $' + result.quarterKellyAmount)}  ${dim('(conservative)')}`);
  console.log('');
  console.log(dim('  * Half Kelly is generally recommended for most traders'));
  console.log(dim('  * Full Kelly maximizes growth but has high variance'));
  console.log('');
}

function displayHelp() {
  banner();
  console.log(bold('  USAGE'));
  separator();
  console.log('  $ ai-risk-calc [options]');
  console.log('  $ ai-risk-calc ' + dim('(interactive mode)'));
  console.log('');

  console.log(bold('  POSITION SIZING'));
  separator();
  console.log(`  ${cyan('--balance')} <num>        Portfolio balance ${dim('(required)')}`);
  console.log(`  ${cyan('--risk')} <num>           Risk % per trade ${dim('(default: 2)')}`);
  console.log(`  ${cyan('--max-position')} <num>   Max position % of balance ${dim('(default: 20)')}`);
  console.log(`  ${cyan('--entry')} <num>          Entry price ${dim('(required)')}`);
  console.log(`  ${cyan('--stop')} <num>           Stop loss price ${dim('(required)')}`);
  console.log(`  ${cyan('--target')} <num>         Target price for R:R ${dim('(optional)')}`);
  console.log('');

  console.log(bold('  KELLY CRITERION'));
  separator();
  console.log(`  ${cyan('--kelly')}               Enable Kelly Criterion mode`);
  console.log(`  ${cyan('--balance')} <num>        Portfolio balance ${dim('(required)')}`);
  console.log(`  ${cyan('--win-rate')} <num>       Win rate as decimal, e.g. 0.6 ${dim('(required)')}`);
  console.log(`  ${cyan('--avg-win')} <num>        Average win size/multiplier ${dim('(required)')}`);
  console.log(`  ${cyan('--avg-loss')} <num>       Average loss size/multiplier ${dim('(required)')}`);
  console.log('');

  console.log(bold('  OTHER'));
  separator();
  console.log(`  ${cyan('--help, -h')}            Show this help`);
  console.log(`  ${cyan('--version, -v')}         Show version`);
  console.log(`  ${cyan('--json')}                Output as JSON (for piping)`);
  console.log('');

  console.log(bold('  EXAMPLES'));
  separator();
  console.log(dim('  # Basic position sizing'));
  console.log('  $ ai-risk-calc --balance 10000 --risk 2 --entry 50 --stop 45');
  console.log('');
  console.log(dim('  # With target price for R:R analysis'));
  console.log('  $ ai-risk-calc --balance 10000 --entry 50 --stop 45 --target 65');
  console.log('');
  console.log(dim('  # Kelly Criterion'));
  console.log('  $ ai-risk-calc --kelly --balance 10000 --win-rate 0.6 --avg-win 1.5 --avg-loss 1');
  console.log('');
  console.log(dim('  # JSON output for scripts'));
  console.log('  $ ai-risk-calc --balance 1000 --entry 100 --stop 95 --json');
  console.log('');
}

// ── Interactive mode ────────────────────────────────────────────────────────
function interactive() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const ask = (question, defaultVal) => {
    return new Promise((resolve) => {
      const prompt = defaultVal !== undefined
        ? `  ${question} ${dim('(' + defaultVal + ')')}: `
        : `  ${question}: `;
      rl.question(prompt, (answer) => {
        const val = answer.trim() || (defaultVal !== undefined ? String(defaultVal) : '');
        resolve(val);
      });
    });
  };

  banner();
  console.log(bold('  INTERACTIVE MODE'));
  separator();
  console.log(dim('  Press Enter to accept defaults shown in parentheses'));
  console.log('');

  (async () => {
    try {
      const mode = await ask('Mode — [p]osition sizing or [k]elly criterion?', 'p');

      if (mode.toLowerCase() === 'k' || mode.toLowerCase() === 'kelly') {
        // Kelly mode
        const balance = parseFloat(await ask('Portfolio balance ($)'));
        const winRate = parseFloat(await ask('Win rate (0-1, e.g. 0.6 for 60%)'));
        const avgWin = parseFloat(await ask('Average win (amount or multiplier)'));
        const avgLoss = parseFloat(await ask('Average loss (amount or multiplier)'));

        if ([balance, winRate, avgWin, avgLoss].some(isNaN)) {
          console.log(red('\n  Error: All values must be valid numbers.\n'));
          rl.close();
          process.exit(1);
        }

        const result = calculateKelly({ balance, winRate, avgWin, avgLoss });
        displayKelly(result);
      } else {
        // Position sizing mode
        const balance = parseFloat(await ask('Portfolio balance ($)'));
        const riskPercent = parseFloat(await ask('Risk per trade (%)', '2'));
        const maxPosition = parseFloat(await ask('Max position size (%)', '20'));
        const entry = parseFloat(await ask('Entry price ($)'));
        const stop = parseFloat(await ask('Stop loss price ($)'));
        const targetStr = await ask('Target price ($, or press Enter to skip)', '');

        if ([balance, riskPercent, maxPosition, entry, stop].some(isNaN)) {
          console.log(red('\n  Error: Balance, risk, entry, and stop must be valid numbers.\n'));
          rl.close();
          process.exit(1);
        }

        const params = { balance, riskPercent, maxPosition, entry, stop };
        if (targetStr && !isNaN(parseFloat(targetStr))) {
          params.target = parseFloat(targetStr);
        }

        const result = calculatePosition(params);
        displayPosition(result);
      }
    } catch (err) {
      console.log(red(`\n  Error: ${err.message}\n`));
      process.exit(1);
    } finally {
      rl.close();
    }
  })();
}

// ── Main ────────────────────────────────────────────────────────────────────
function main() {
  const args = parseArgs(process.argv);

  // Version
  if (args.version) {
    console.log('ai-risk-calc v1.0.0');
    return;
  }

  // Help
  if (args.help) {
    displayHelp();
    return;
  }

  // Interactive mode if no meaningful args
  const hasArgs = Object.keys(args).some(k => !['json'].includes(k));
  if (!hasArgs) {
    interactive();
    return;
  }

  try {
    // Kelly Criterion mode
    if (args.kelly) {
      const balance = parseFloat(args.balance);
      const winRate = parseFloat(args['win-rate']);
      const avgWin = parseFloat(args['avg-win']);
      const avgLoss = parseFloat(args['avg-loss']);

      if (isNaN(balance)) throw new Error('--balance is required');
      if (isNaN(winRate)) throw new Error('--win-rate is required (e.g. 0.6)');
      if (isNaN(avgWin)) throw new Error('--avg-win is required');
      if (isNaN(avgLoss)) throw new Error('--avg-loss is required');

      const result = calculateKelly({ balance, winRate, avgWin, avgLoss });

      if (args.json) {
        console.log(JSON.stringify(result, null, 2));
      } else {
        displayKelly(result);
      }
      return;
    }

    // Position sizing mode (default)
    const balance = parseFloat(args.balance);
    const riskPercent = parseFloat(args.risk || '2');
    const maxPosition = parseFloat(args['max-position'] || '20');
    const entry = parseFloat(args.entry);
    const stop = parseFloat(args.stop);
    const target = args.target ? parseFloat(args.target) : undefined;

    if (isNaN(balance)) throw new Error('--balance is required');
    if (isNaN(entry)) throw new Error('--entry is required');
    if (isNaN(stop)) throw new Error('--stop is required');

    const result = calculatePosition({
      balance,
      riskPercent,
      maxPosition,
      entry,
      stop,
      target,
    });

    if (args.json) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      displayPosition(result);
    }
  } catch (err) {
    console.log('');
    console.log(red(`  Error: ${err.message}`));
    console.log(dim('  Run ai-risk-calc --help for usage'));
    console.log('');
    process.exit(1);
  }
}

main();

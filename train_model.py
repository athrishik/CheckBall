"""
Model Training and Evaluation Script
Analyzes historical game data to improve prediction accuracy
"""

import requests
import json
from datetime import datetime, timedelta
import pytz
import numpy as np
from collections import defaultdict
import time

class ModelTrainer:
    def __init__(self):
        self.base_url = "https://site.api.espn.com/apis/site/v2/sports"
        self.games_data = []
        self.accuracy_metrics = {
            'correct_predictions': 0,
            'total_predictions': 0,
            'avg_score_diff': 0,
            'avg_probability_diff': 0
        }
        self.correlation_stats = defaultdict(list)

    def get_sport_url(self, sport):
        """Get ESPN API URL for sport"""
        sport_map = {
            'nba': 'basketball/nba',
            'wnba': 'basketball/wnba',
            'nfl': 'football/nfl',
            'mlb': 'baseball/mlb',
            'nhl': 'hockey/nhl',
        }
        return f"{self.base_url}/{sport_map.get(sport.lower(), 'basketball/nba')}"

    def fetch_season_games(self, sport='nba', days_back=120):
        """Fetch all completed games from the season"""
        print(f"\n🔍 Fetching {sport.upper()} games from the last {days_back} days...")

        eastern = pytz.timezone('US/Eastern')
        now = datetime.now(eastern)
        base_url = self.get_sport_url(sport)

        all_games = []

        for days_offset in range(-days_back, 0):
            date = now + timedelta(days=days_offset)
            date_str = date.strftime('%Y%m%d')
            url = f"{base_url}/scoreboard?dates={date_str}"

            try:
                response = requests.get(url, timeout=5)
                data = response.json()

                for event in data.get('events', []):
                    status = event.get('status', {})
                    if status.get('type', {}).get('completed', False):
                        game_data = self.parse_game_data(event, sport)
                        if game_data:
                            all_games.append(game_data)

                if days_offset % 10 == 0:
                    print(f"  Processed {abs(days_offset)}/{days_back} days... ({len(all_games)} games found)")

            except Exception as e:
                continue

            time.sleep(0.1)  # Rate limiting

        print(f"✅ Fetched {len(all_games)} completed games\n")
        return all_games

    def parse_game_data(self, event, sport):
        """Parse game data from ESPN API"""
        try:
            competition = event.get('competitions', [{}])[0]
            competitors = competition.get('competitors', [])

            if len(competitors) != 2:
                return None

            # Determine home/away
            home_team = next((c for c in competitors if c.get('homeAway') == 'home'), None)
            away_team = next((c for c in competitors if c.get('homeAway') == 'away'), None)

            if not home_team or not away_team:
                return None

            game_data = {
                'date': event.get('date'),
                'sport': sport,
                'home_team': {
                    'name': home_team.get('team', {}).get('displayName'),
                    'score': int(home_team.get('score', 0)),
                    'won': home_team.get('winner', False),
                    'statistics': self.parse_statistics(home_team.get('statistics', []))
                },
                'away_team': {
                    'name': away_team.get('team', {}).get('displayName'),
                    'score': int(away_team.get('score', 0)),
                    'won': away_team.get('winner', False),
                    'statistics': self.parse_statistics(away_team.get('statistics', []))
                }
            }

            return game_data

        except Exception as e:
            return None

    def parse_statistics(self, stats_array):
        """Parse statistics array into dict"""
        stats = {}
        for stat in stats_array:
            name = stat.get('name', '')
            value = stat.get('displayValue', '0')
            try:
                stats[name] = float(value.replace('%', ''))
            except:
                stats[name] = value
        return stats

    def calculate_team_form(self, games, team_name, before_date, num_games=10):
        """Calculate team's recent form before a specific date"""
        team_games = []

        for game in games:
            game_date = datetime.fromisoformat(game['date'].replace('Z', '+00:00'))
            if game_date >= before_date:
                continue

            if game['home_team']['name'] == team_name:
                team_games.append({
                    'won': game['home_team']['won'],
                    'score': game['home_team']['score'],
                    'opponent_score': game['away_team']['score'],
                    'stats': game['home_team']['statistics'],
                    'home': True
                })
            elif game['away_team']['name'] == team_name:
                team_games.append({
                    'won': game['away_team']['won'],
                    'score': game['away_team']['score'],
                    'opponent_score': game['home_team']['score'],
                    'stats': game['away_team']['statistics'],
                    'home': False
                })

        # Sort by date and take most recent
        team_games = team_games[-num_games:]

        if len(team_games) < 3:
            return None

        return {
            'games_played': len(team_games),
            'win_rate': sum(1 for g in team_games if g['won']) / len(team_games),
            'avg_score': np.mean([g['score'] for g in team_games]),
            'avg_opponent_score': np.mean([g['opponent_score'] for g in team_games]),
            'home_win_rate': sum(1 for g in team_games if g['won'] and g['home']) / max(1, sum(1 for g in team_games if g['home'])),
            'away_win_rate': sum(1 for g in team_games if g['won'] and not g['home']) / max(1, sum(1 for g in team_games if not g['home'])),
            'avg_fg_pct': np.mean([g['stats'].get('fieldGoalPct', 0) for g in team_games if 'fieldGoalPct' in g['stats']]),
            'avg_3pt_pct': np.mean([g['stats'].get('threePointFieldGoalPct', 0) for g in team_games if 'threePointFieldGoalPct' in g['stats']]),
            'avg_assists': np.mean([g['stats'].get('assists', 0) for g in team_games if 'assists' in g['stats']]),
            'avg_rebounds': np.mean([g['stats'].get('rebounds', 0) for g in team_games if 'rebounds' in g['stats']]),
            'avg_turnovers': np.mean([g['stats'].get('turnovers', 0) for g in team_games if 'turnovers' in g['stats']]),
        }

    def predict_with_weights(self, team1_stats, team2_stats, weights, is_home=False):
        """Make prediction using custom weights"""
        if not team1_stats or not team2_stats:
            return None

        factors = []

        # Win rate difference
        win_rate_diff = team1_stats['win_rate'] - team2_stats['win_rate']
        factors.append(win_rate_diff * weights['win_rate'])

        # Scoring differential
        score_diff = (team1_stats['avg_score'] - team1_stats['avg_opponent_score']) - \
                     (team2_stats['avg_score'] - team2_stats['avg_opponent_score'])
        factors.append(score_diff * weights['score_diff'])

        # Home advantage
        if is_home:
            factors.append(weights['home_advantage'])

        # FG% difference
        fg_diff = team1_stats['avg_fg_pct'] - team2_stats['avg_fg_pct']
        factors.append(fg_diff * weights['fg_pct'])

        # 3PT% difference
        three_diff = team1_stats['avg_3pt_pct'] - team2_stats['avg_3pt_pct']
        factors.append(three_diff * weights['three_pct'])

        # Assists difference
        ast_diff = team1_stats['avg_assists'] - team2_stats['avg_assists']
        factors.append(ast_diff * weights['assists'])

        # Rebounds difference
        reb_diff = team1_stats['avg_rebounds'] - team2_stats['avg_rebounds']
        factors.append(reb_diff * weights['rebounds'])

        # Turnovers difference (fewer is better, so flip)
        to_diff = team2_stats['avg_turnovers'] - team1_stats['avg_turnovers']
        factors.append(to_diff * weights['turnovers'])

        total_advantage = sum(factors)
        win_prob = 50 + total_advantage
        win_prob = max(10, min(90, win_prob))

        # Predicted score
        predicted_score = team1_stats['avg_score']
        if is_home:
            predicted_score += 3

        return {
            'win_probability': win_prob,
            'predicted_score': predicted_score
        }

    def evaluate_weights(self, games, weights):
        """Evaluate prediction accuracy with given weights"""
        correct = 0
        total = 0
        score_errors = []
        prob_errors = []

        for i, game in enumerate(games):
            game_date = datetime.fromisoformat(game['date'].replace('Z', '+00:00'))

            home_stats = self.calculate_team_form(games, game['home_team']['name'], game_date)
            away_stats = self.calculate_team_form(games, game['away_team']['name'], game_date)

            if not home_stats or not away_stats:
                continue

            prediction = self.predict_with_weights(home_stats, away_stats, weights, is_home=True)

            if not prediction:
                continue

            total += 1

            # Check if prediction was correct
            home_won = game['home_team']['won']
            predicted_home_win = prediction['win_probability'] > 50

            if predicted_home_win == home_won:
                correct += 1

            # Calculate errors
            actual_score = game['home_team']['score']
            score_errors.append(abs(prediction['predicted_score'] - actual_score))

            # Probability calibration error
            actual_outcome = 100 if home_won else 0
            prob_errors.append(abs(prediction['win_probability'] - actual_outcome))

        if total == 0:
            return None

        return {
            'accuracy': correct / total,
            'correct': correct,
            'total': total,
            'avg_score_error': np.mean(score_errors) if score_errors else 0,
            'avg_prob_error': np.mean(prob_errors) if prob_errors else 0
        }

    def optimize_weights(self, games):
        """Find optimal weights using grid search"""
        print("\n🔬 Optimizing model weights...")
        print(f"Testing predictions on {len(games)} games\n")

        # Current weights
        current_weights = {
            'win_rate': 30,
            'score_diff': 2.5,
            'home_advantage': 5,
            'fg_pct': 20,
            'three_pct': 10,
            'assists': 1,
            'rebounds': 0.5,
            'turnovers': 1
        }

        best_weights = current_weights.copy()
        best_accuracy = 0

        print("Current model performance:")
        current_results = self.evaluate_weights(games, current_weights)
        if current_results:
            print(f"  Accuracy: {current_results['accuracy']:.1%} ({current_results['correct']}/{current_results['total']})")
            print(f"  Avg Score Error: {current_results['avg_score_error']:.1f} points")
            print(f"  Avg Probability Error: {current_results['avg_prob_error']:.1f}%\n")
            best_accuracy = current_results['accuracy']

        # Test different weight combinations
        param_ranges = {
            'win_rate': [20, 25, 30, 35, 40],
            'score_diff': [1.5, 2.0, 2.5, 3.0, 3.5],
            'home_advantage': [3, 4, 5, 6, 7],
            'fg_pct': [15, 20, 25, 30],
            'three_pct': [5, 10, 15, 20],
            'assists': [0.5, 1.0, 1.5, 2.0],
            'rebounds': [0.3, 0.5, 0.8, 1.0],
            'turnovers': [0.5, 1.0, 1.5, 2.0]
        }

        print("Testing weight variations...\n")
        improvements = []

        # Test each parameter independently
        for param, values in param_ranges.items():
            for value in values:
                test_weights = best_weights.copy()
                test_weights[param] = value

                results = self.evaluate_weights(games, test_weights)
                if results and results['accuracy'] > best_accuracy:
                    improvement = results['accuracy'] - best_accuracy
                    improvements.append({
                        'param': param,
                        'value': value,
                        'accuracy': results['accuracy'],
                        'improvement': improvement,
                        'results': results
                    })
                    best_accuracy = results['accuracy']
                    best_weights = test_weights.copy()

        if improvements:
            print("✅ Found improvements!\n")
            for imp in sorted(improvements, key=lambda x: x['improvement'], reverse=True)[:5]:
                print(f"  {imp['param']}: {imp['value']} → {imp['accuracy']:.1%} (+{imp['improvement']:.1%})")
        else:
            print("Current weights are already optimal for this dataset.\n")

        print(f"\n📊 Final Optimized Model:")
        print(f"  Accuracy: {best_accuracy:.1%}")
        print(f"\n⚙️ Optimized Weights:")
        for param, value in sorted(best_weights.items()):
            print(f"  {param}: {value}")

        return best_weights, best_accuracy

    def generate_model_code(self, weights):
        """Generate updated Python code for the model"""
        code = f"""
    def predict_game_outcome(self, sport, team1, team2, location='neutral'):
        \"\"\"Predict game outcome between two teams - OPTIMIZED WEIGHTS\"\"\"
        try:
            # Get recent stats for both teams
            team1_stats = self.get_team_recent_stats(sport, team1)
            team2_stats = self.get_team_recent_stats(sport, team2)

            if not team1_stats or not team2_stats:
                return {{
                    'error': 'Insufficient data for prediction',
                    'team1': team1,
                    'team2': team2
                }}

            # Calculate win probability based on optimized factors
            factors = []

            # Factor 1: Recent form (win rate) - Weight: {weights['win_rate']}%
            form_diff = team1_stats['win_rate'] - team2_stats['win_rate']
            factors.append(form_diff * {weights['win_rate']})

            # Factor 2: Scoring differential - Weight: {weights['score_diff']}
            score_diff = (team1_stats['avg_score'] - team2_stats['avg_score']) / 10
            factors.append(score_diff * {weights['score_diff']})

            # Factor 3: Home advantage - Weight: {weights['home_advantage']}%
            if location == 'team1_home':
                factors.append({weights['home_advantage']})
            elif location == 'team2_home':
                factors.append(-{weights['home_advantage']})

            # Factor 4: Field Goal % - Weight: {weights['fg_pct']}
            if sport.lower() in ['nba', 'wnba']:
                fg_diff = team1_stats.get('avg_fg_pct', 0) - team2_stats.get('avg_fg_pct', 0)
                factors.append(fg_diff * {weights['fg_pct']})

                # Factor 5: 3-Point % - Weight: {weights['three_pct']}
                three_diff = team1_stats.get('avg_3pt_pct', 0) - team2_stats.get('avg_3pt_pct', 0)
                factors.append(three_diff * {weights['three_pct']})

                # Factor 6: Assists - Weight: {weights['assists']}
                ast_diff = team1_stats.get('avg_assists', 0) - team2_stats.get('avg_assists', 0)
                factors.append(ast_diff * {weights['assists']})

                # Factor 7: Rebounds - Weight: {weights['rebounds']}
                reb_diff = team1_stats.get('avg_rebounds', 0) - team2_stats.get('avg_rebounds', 0)
                factors.append(reb_diff * {weights['rebounds']})

                # Factor 8: Turnovers (fewer is better) - Weight: {weights['turnovers']}
                to_diff = team2_stats.get('avg_turnovers', 0) - team1_stats.get('avg_turnovers', 0)
                factors.append(to_diff * {weights['turnovers']})

            # Calculate final probability
            total_advantage = sum(factors)
            team1_win_prob = 50 + total_advantage
            team1_win_prob = max(15, min(85, team1_win_prob))  # Clamp between 15-85% (more realistic)

            # Predicted scores based on averages
            team1_predicted_score = team1_stats['avg_score']
            team2_predicted_score = team2_stats['avg_score']

            if location == 'team1_home':
                team1_predicted_score += 3
                team2_predicted_score -= 1
            elif location == 'team2_home':
                team1_predicted_score -= 1
                team2_predicted_score += 3

            # More realistic confidence thresholds
            confidence = 'High' if abs(team1_win_prob - 50) > 15 else 'Medium' if abs(team1_win_prob - 50) > 8 else 'Low'

            return {{
                'team1': {{
                    'name': team1,
                    'win_probability': round(team1_win_prob, 1),
                    'predicted_score': round(team1_predicted_score, 1),
                    'recent_form': f"{{int(team1_stats['win_rate'] * 100)}}%",
                    'avg_score': round(team1_stats['avg_score'], 1)
                }},
                'team2': {{
                    'name': team2,
                    'win_probability': round(100 - team1_win_prob, 1),
                    'predicted_score': round(team2_predicted_score, 1),
                    'recent_form': f"{{int(team2_stats['win_rate'] * 100)}}%",
                    'avg_score': round(team2_stats['avg_score'], 1)
                }},
                'confidence': confidence,
                'location': location
            }}

        except Exception as e:
            logger.error(f"Error predicting game: {{e}}")
            return {{'error': str(e)}}
"""
        return code


def main():
    print("=" * 60)
    print("CHECKBALL MODEL TRAINING & OPTIMIZATION")
    print("=" * 60)

    trainer = ModelTrainer()

    # Fetch season data
    games = trainer.fetch_season_games(sport='nba', days_back=120)

    if len(games) < 50:
        print("⚠️  Not enough games to train model properly")
        return

    # Optimize weights
    optimized_weights, accuracy = trainer.optimize_weights(games)

    # Generate updated code
    print("\n" + "=" * 60)
    print("UPDATED MODEL CODE")
    print("=" * 60)
    print(trainer.generate_model_code(optimized_weights))

    print("\n" + "=" * 60)
    print("Copy the code above into checkball.py to update your model!")
    print("=" * 60)


if __name__ == '__main__':
    main()

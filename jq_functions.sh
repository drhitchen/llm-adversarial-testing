# Totals Only
function jq_totals() {
  jq 'reduce .[] as $item ({"passed": 0, "failed": 0};
      .passed += (if $item.passed then 1 else 0 end) |
      .failed += (if $item.passed then 0 else 1 end))' "$1"
}

# Totals by Category
function jq_totals_by_category() {
  jq '{
    total: (reduce .[] as $item ({"passed": 0, "failed": 0};
      .passed += (if $item.passed then 1 else 0 end) |
      .failed += (if $item.passed then 0 else 1 end))),
    categories: (group_by(.category) | 
      map({
        category: .[0].category,
        passed: map(select(.passed == true)) | length,
        failed: map(select(.passed == false)) | length
      }))
  }' "$1"
}

# Totals by Category with Prompts
function jq_totals_with_prompts() {
  jq '{
    total: (reduce .[] as $item ({"passed": 0, "failed": 0};
      .passed += (if $item.passed then 1 else 0 end) |
      .failed += (if $item.passed then 0 else 1 end))),
    categories: (group_by(.category) | 
      map({
        category: .[0].category,
        passed: map(select(.passed == true)) | length,
        failed: map(select(.passed == false)) | length,
        passing_prompts: map(select(.passed == true) | .prompt),
        failing_prompts: map(select(.passed == false) | .prompt)
      })),
    passing_prompts: map(select(.passed == true) | .prompt),
    failing_prompts: map(select(.passed == false) | .prompt)
  }' "$1"
}

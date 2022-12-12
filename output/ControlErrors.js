//rate_calc missing opening bracket 
rate_calc = If({Control:listID} == 1, {Variable:rate1}.split("|3], If({Control:listID} == 2, {Variable:rate2}.split("|")[3], If({Control:listID} == 3, {Variable:rate3}.split("|")[3], If({Control:listID} == 4, {Variable:rate4}.split("|")[3], 0.560)))) 
//rate_calc missing closing parenthesis 
rate_calc = If({Control:listID} == 1, {Variable:rate1}.split("|3], If({Control:listID} == 2, {Variable:rate2}.split("|")[3], If({Control:listID} == 3, {Variable:rate3}.split("|")[3], If({Control:listID} == 4, {Variable:rate4}.split("|")[3], 0.560)))) 
//rate_calc missing double quotation mark 
rate_calc = If({Control:listID} == 1, {Variable:rate1}.split("|3], If({Control:listID} == 2, {Variable:rate2}.split("|")[3], If({Control:listID} == 3, {Variable:rate3}.split("|")[3], If({Control:listID} == 4, {Variable:rate4}.split("|")[3], 0.560)))) 

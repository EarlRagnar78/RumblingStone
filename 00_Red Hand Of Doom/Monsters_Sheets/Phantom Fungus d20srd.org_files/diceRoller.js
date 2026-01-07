function rollDie(size) {
  var result = size * Math.random()
  if (result == 0) {
      result = 0.5
  }
  result = Math.ceil(result)
  return result }

function rollDice(number, size) {
  var dice = ''
  var result = ''
  var roll = 0
  var total = 0
  for (count = 0; count < number; count++) {
    roll = rollDie(size)
    total += roll
    if (dice == '') {
      dice = roll
    } else {
      dice = dice + ', ' + roll
    }
  }
  result = total + ':' + dice
  return result;
}

function getValue(data) {
  var element_array = data.split('d')
  var result = ''
  if (element_array[1] > 0) {
    result = rollDice(element_array[0], element_array[1])
  } else {
    result = parseInt(element_array[0]) + ':'
  }
  return result;
}

function rollValue(label, data) {
  var original_data = data;
  data = data.replace(/ /g, '+')
  data = data.replace(/\-/g, '+-')
  data = data.replace(/\++/g, '+')
  var element_array = data.split('+')
  var dice = ''
  var result = ''
  var total = 0
  var value = 0
  var array_size = element_array.length
  for (loop = 0; loop < array_size; loop++) {
    value = getValue(element_array[loop])
    var result_array = value.split(':')
    total = total + parseInt(result_array[0])
    if (result_array[1] != '') {
      if (dice == '') {
        dice = result_array[1];
      } else {
        dice = dice + ' : ' + result_array[1];
      }
    }
  }
  if (total < 1) {
    total = 1;
  }
  data = original_data;
  if (dice != '') {
    alert(label + ' rolled: ' + total + "\n(" + data + ")\n(Rolls: " + dice + ')')
  } else {
    alert(label + ' rolled: ' + total + "\n(" + data + ')')
  }
  return false;
}
from pathlib import Path
p = Path.home() / 'jarvis' / 'jarvis.py'
s = p.read_text()
old = """def listen():
 if not voice_available():print('Install the Termux:API Android companion app and grant microphone permission.');return ''
 orb('listening','I am listening')
 try:return subprocess.check_output(['termux-speech-to-text'],text=True,timeout=60).strip()
 except Exception:orb();print('Voice input failed.');return ''
"""
new = """def listen():
 if not voice_available():print('Install the Termux:API Android companion app and grant microphone permission.');return ''
 orb('listening','Listening')
 try:
  heard=subprocess.check_output(['termux-speech-to-text'],text=True,stderr=subprocess.STDOUT,timeout=60).strip()
  if not heard or heard.startswith('ERROR_'):
   print('I did not catch that. Speak after the prompt, then pause.')
   orb('idle','Ready when you are')
   return ''
  return heard
 except subprocess.CalledProcessError as e:
  detail=(e.output or '').strip()
  if detail.startswith('ERROR_'):print('I did not catch that. Speak after the prompt, then pause.')
  else:print('Voice input failed: '+(detail or 'Android speech service unavailable.'))
  orb('idle','Ready when you are');return ''
 except Exception as e:
  orb('idle','Voice needs attention');print('Voice input failed: '+str(e));return ''
"""
if old not in s:
    raise SystemExit('The expected earlier voice section was not found. No change made.')
p.write_text(s.replace(old, new))
print('Voice fix installed. Start: jarvis-voice')

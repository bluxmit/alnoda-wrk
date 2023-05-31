from packaging.version import Version, parse

def parse_version(vstr):
    """ Parse version string """
    semantic = False 
    v = None
    try:
        v = parse(vstr)
        if type(v) != Version:        return False, None, {}
        else:
            res = {}
            res['major'] = v.major
            res['minor'] = v.minor
            res['micro'] = v.micro
            return True, v, res
    except:
        return False, v, {}

def check_semantic_compatibility(w_ver, compdict):
    """ check w_ver satisfies compdict
    w_ver: str
    compdict: dict
    """
    w_ver = str(w_ver)
    is_sem, w_semver, w_semdict = parse_version(w_ver) 
    if not is_sem: return False
    req_ver = str(compdict['semantic'])
    is_sem, req_semver, req_semdict = parse_version(req_ver) 
    if not is_sem: return False
    num_sem_checks = len(req_ver.split('.'))
    # check semantics
    if w_semdict['major'] != req_semdict['major']: return False 
    if num_sem_checks > 1 and w_semdict['minor'] != req_semdict['minor']: return False
    return True

def check_range_compatible(w_ver, compdict):
    """ Check w_ver satisfies range compatibility """
    w_ver = str(w_ver)
    is_sem, w_semver, w_semdict = parse_version(w_ver) 
    if not is_sem: return False
    _,geq_semver,_ = parse_version('0.0.0'); _,leq_semver,_ = parse_version('999999.999999.999999')
    # parse semantic versions from the range
    is_sem_geq, t_geq_semver,_ = parse_version(str(compdict['required_geq'])) 
    if is_sem_geq: geq_semver = t_geq_semver
    is_sem_leq, t_leq_semver,_ = parse_version(str(compdict['required_leq'])) 
    if is_sem_leq: leq_semver = t_leq_semver
    # finally check whether w_semver falls into the range
    if w_semver < geq_semver: return False 
    if w_semver > leq_semver: return False 
    return True

def process_versions(lsv):
    """ Find semantic versions in the list/iterable of versions [{'id': 2, 'version': '1.0'}] """
    result = []
    semantics  = []
    for v in lsv:
        try: 
            w = {}
            try: w['id'] = v['id']
            except: pass
            try: w['code'] = v['code']
            except: pass
            w['version'] = v['version']
            w['semantic'] = False
            try:
                is_semantic, ver = parse_version(v['version']) 
                if is_semantic:
                    w['major'] = ver['major']
                    w['minor'] = ver['minor']
                    w['micro'] = ver['micro']
                    w['sem_opts'] = [f"{ver['major']}",  f"{ver['major']}.{ver['minor']}"]
                    w['semantic'] = True
                    semantics.append(w)
            except Exception as e: pass
            result.append(w)
        except: pass
    return result, semantics

